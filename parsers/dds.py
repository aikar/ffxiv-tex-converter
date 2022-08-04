# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum, IntFlag


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Dds(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.hdr = Dds.Header(self._io, self, self._root)
        self.bd = Dds.Body(self._io, self, self._root)

    class Header(KaitaiStruct):
        """
        .. seealso::
           Source - https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dds-header
        """

        class FormatFlags(IntFlag):
            ddsd_caps = 1
            ddsd_height = 2
            ddsd_width = 4
            ddsd_pitch = 8
            ddsd_pixelformat = 65536
            ddsd_mipmapcount = 131072
            ddsd_linearsize = 524288
            ddsd_depth = 8388608

        class CapsFlags(IntFlag):
            ddscaps_complex = 8
            ddscaps_texture = 4096
            ddscaps_mipmap = 4194304

        class Caps2Flags(IntFlag):
            ddscaps2_cubemap = 512
            ddscaps2_cubemap_positivex = 1024
            ddscaps2_cubemap_negativex = 2048
            ddscaps2_cubemap_positivey = 4096
            ddscaps2_cubemap_negativey = 8192
            ddscaps2_cubemap_positivez = 16384
            ddscaps2_cubemap_negativez = 32768
            ddscaps2_volume = 2097152
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x44\x44\x53\x20":
                raise kaitaistruct.ValidationNotEqualError(b"\x44\x44\x53\x20", self.magic, self._io, u"/types/header/seq/0")
            self.size = self._io.read_u4le()
            self.flags = KaitaiStream.resolve_enum(Dds.Header.FormatFlags, self._io.read_u4le())
            self.height = self._io.read_u4le()
            self.width = self._io.read_u4le()
            self.pitch_or_linear_size = self._io.read_u4le()
            self.depth = self._io.read_u4le()
            self.mip_map_count = self._io.read_u4le()
            self.reserved1 = self._io.read_bytes(44)
            self.ddspf = Dds.DdsPixelformat(self._io, self, self._root)
            self.caps = KaitaiStream.resolve_enum(Dds.Header.CapsFlags, self._io.read_u4le())
            self.caps2 = KaitaiStream.resolve_enum(Dds.Header.Caps2Flags, self._io.read_u4le())
            self.caps3 = self._io.read_bytes(4)
            self.caps4 = self._io.read_bytes(4)
            self.reserved2 = self._io.read_bytes(4)


    class DdsPixelformat(KaitaiStruct):

        class PixelFormats(IntFlag):
            none = 0
            dx10 = 808540228
            dxt1 = 827611204
            dxt3 = 861165636
            dxt5 = 894720068

        class FormatFlags(Enum):
            ddpf_alphapixels = 1
            ddpf_alpha = 2
            ddpf_mipmap = 4
            ddpf_rgb = 64
            ddpf_yuv = 512
            ddpf_luminance = 131072
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.size = self._io.read_u4le()
            self.flags = KaitaiStream.resolve_enum(Dds.DdsPixelformat.FormatFlags, self._io.read_u4le())
            self.fourcc = KaitaiStream.resolve_enum(Dds.DdsPixelformat.PixelFormats, self._io.read_u4le())
            self.rgb_bit_count = self._io.read_u4le()
            self.r_bit_mask = self._io.read_bytes(4)
            self.g_bit_mask = self._io.read_bytes(4)
            self.b_bit_mask = self._io.read_bytes(4)
            self.a_bit_mask = self._io.read_bytes(4)


    class Body(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(self._io.read_bytes(4))
                i += 1




