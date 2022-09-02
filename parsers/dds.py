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
        if self.fourcc == 808540228:
            self.hdr_dxt10 = Dds.HeaderDxt10(self._io, self, self._root)

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
            ddsd_pixelformat = 4096
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
            self.mipmap_count = self._io.read_u4le()
            self.reserved1 = self._io.read_bytes(44)
            self.ddspf = Dds.DdsPixelformat(self._io, self, self._root)
            self.caps = KaitaiStream.resolve_enum(Dds.Header.CapsFlags, self._io.read_u4le())
            self.caps2 = KaitaiStream.resolve_enum(Dds.Header.Caps2Flags, self._io.read_u4le())
            self.caps3 = self._io.read_bytes(4)
            self.caps4 = self._io.read_bytes(4)
            self.reserved2 = self._io.read_bytes(4)


    class DdsPixelformat(KaitaiStruct):

        class PixelFormats(Enum):
            none = 0
            dx10 = 808540228
            dxt1 = 827611204
            dxt3 = 861165636
            dxt5 = 894720068

        class FormatFlags(Enum):
            ddpf_alphapixels = 1
            ddpf_alpha = 2
            ddpf_fourcc = 4
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


    class HeaderDxt10(KaitaiStruct):

        class DxgiFormats(Enum):
            dxgi_format_unknown = 0
            dxgi_format_r32g32b32a32_typeless = 1
            dxgi_format_r32g32b32a32_float = 2
            dxgi_format_r32g32b32a32_uint = 3
            dxgi_format_r32g32b32a32_sint = 4
            dxgi_format_r32g32b32_typeless = 5
            dxgi_format_r32g32b32_float = 6
            dxgi_format_r32g32b32_uint = 7
            dxgi_format_r32g32b32_sint = 8
            dxgi_format_r16g16b16a16_typeless = 9
            dxgi_format_r16g16b16a16_float = 10
            dxgi_format_r16g16b16a16_unorm = 11
            dxgi_format_r16g16b16a16_uint = 12
            dxgi_format_r16g16b16a16_snorm = 13
            dxgi_format_r16g16b16a16_sint = 14
            dxgi_format_r32g32_typeless = 15
            dxgi_format_r32g32_float = 16
            dxgi_format_r32g32_uint = 17
            dxgi_format_r32g32_sint = 18
            dxgi_format_r32g8x24_typeless = 19
            dxgi_format_d32_float_s8x24_uint = 20
            dxgi_format_r32_float_x8x24_typeless = 21
            dxgi_format_x32_typeless_g8x24_uint = 22
            dxgi_format_r10g10b10a2_typeless = 23
            dxgi_format_r10g10b10a2_unorm = 24
            dxgi_format_r10g10b10a2_uint = 25
            dxgi_format_r11g11b10_float = 26
            dxgi_format_r8g8b8a8_typeless = 27
            dxgi_format_r8g8b8a8_unorm = 28
            dxgi_format_r8g8b8a8_unorm_srgb = 29
            dxgi_format_r8g8b8a8_uint = 30
            dxgi_format_r8g8b8a8_snorm = 31
            dxgi_format_r8g8b8a8_sint = 32
            dxgi_format_r16g16_typeless = 33
            dxgi_format_r16g16_float = 34
            dxgi_format_r16g16_unorm = 35
            dxgi_format_r16g16_uint = 36
            dxgi_format_r16g16_snorm = 37
            dxgi_format_r16g16_sint = 38
            dxgi_format_r32_typeless = 39
            dxgi_format_d32_float = 40
            dxgi_format_r32_float = 41
            dxgi_format_r32_uint = 42
            dxgi_format_r32_sint = 43
            dxgi_format_r24g8_typeless = 44
            dxgi_format_d24_unorm_s8_uint = 45
            dxgi_format_r24_unorm_x8_typeless = 46
            dxgi_format_x24_typeless_g8_uint = 47
            dxgi_format_r8g8_typeless = 48
            dxgi_format_r8g8_unorm = 49
            dxgi_format_r8g8_uint = 50
            dxgi_format_r8g8_snorm = 51
            dxgi_format_r8g8_sint = 52
            dxgi_format_r16_typeless = 53
            dxgi_format_r16_float = 54
            dxgi_format_d16_unorm = 55
            dxgi_format_r16_unorm = 56
            dxgi_format_r16_uint = 57
            dxgi_format_r16_snorm = 58
            dxgi_format_r16_sint = 59
            dxgi_format_r8_typeless = 60
            dxgi_format_r8_unorm = 61
            dxgi_format_r8_uint = 62
            dxgi_format_r8_snorm = 63
            dxgi_format_r8_sint = 64
            dxgi_format_a8_unorm = 65
            dxgi_format_r1_unorm = 66
            dxgi_format_r9g9b9e5_sharedexp = 67
            dxgi_format_r8g8_b8g8_unorm = 68
            dxgi_format_g8r8_g8b8_unorm = 69
            dxgi_format_bc1_typeless = 70
            dxgi_format_bc1_unorm = 71
            dxgi_format_bc1_unorm_srgb = 72
            dxgi_format_bc2_typeless = 73
            dxgi_format_bc2_unorm = 74
            dxgi_format_bc2_unorm_srgb = 75
            dxgi_format_bc3_typeless = 76
            dxgi_format_bc3_unorm = 77
            dxgi_format_bc3_unorm_srgb = 78
            dxgi_format_bc4_typeless = 79
            dxgi_format_bc4_unorm = 80
            dxgi_format_bc4_snorm = 81
            dxgi_format_bc5_typeless = 82
            dxgi_format_bc5_unorm = 83
            dxgi_format_bc5_snorm = 84
            dxgi_format_b5g6r5_unorm = 85
            dxgi_format_b5g5r5a1_unorm = 86
            dxgi_format_b8g8r8a8_unorm = 87
            dxgi_format_b8g8r8x8_unorm = 88
            dxgi_format_r10g10b10_xr_bias_a2_unorm = 89
            dxgi_format_b8g8r8a8_typeless = 90
            dxgi_format_b8g8r8a8_unorm_srgb = 91
            dxgi_format_b8g8r8x8_typeless = 92
            dxgi_format_b8g8r8x8_unorm_srgb = 93
            dxgi_format_bc6h_typeless = 94
            dxgi_format_bc6h_uf16 = 95
            dxgi_format_bc6h_sf16 = 96
            dxgi_format_bc7_typeless = 97
            dxgi_format_bc7_unorm = 98
            dxgi_format_bc7_unorm_srgb = 99
            dxgi_format_ayuv = 100
            dxgi_format_y410 = 101
            dxgi_format_y416 = 102
            dxgi_format_nv12 = 103
            dxgi_format_p010 = 104
            dxgi_format_p016 = 105
            dxgi_format_420_opaque = 106
            dxgi_format_yuy2 = 107
            dxgi_format_y210 = 108
            dxgi_format_y216 = 109
            dxgi_format_nv11 = 110
            dxgi_format_ai44 = 111
            dxgi_format_ia44 = 112
            dxgi_format_p8 = 113
            dxgi_format_a8p8 = 114
            dxgi_format_b4g4r4a4_unorm = 115
            dxgi_format_p208 = 130
            dxgi_format_v208 = 131
            dxgi_format_v408 = 132
            dxgi_format_sampler_feedback_min_mip_opaque = 189
            dxgi_format_sampler_feedback_mip_region_used_opaque = 190
            dxgi_format_force_uint = 4294967295

        class D3d10ResourceDimensionFormats(Enum):
            d3d10_resource_dimension_unknown = 0
            d3d10_resource_dimension_buffer = 1
            d3d10_resource_dimension_texture1d = 2
            d3d10_resource_dimension_texture2d = 3
            d3d10_resource_dimension_texture3d = 4

        class D3d11ResourceMiscFlags(Enum):
            d3d11_resource_misc_generate_mips = 1
            d3d11_resource_misc_shared = 2
            d3d11_resource_misc_texturecube = 4
            d3d11_resource_misc_drawindirect_args = 16
            d3d11_resource_misc_buffer_allow_raw_views = 32
            d3d11_resource_misc_buffer_structured = 64
            d3d11_resource_misc_resource_clamp = 128
            d3d11_resource_misc_shared_keyedmutex = 256
            d3d11_resource_misc_gdi_compatible = 512
            d3d11_resource_misc_shared_nthandle = 2048
            d3d11_resource_misc_restricted_content = 4096
            d3d11_resource_misc_restrict_shared_resource = 8192
            d3d11_resource_misc_restrict_shared_resource_driver = 16384
            d3d11_resource_misc_guarded = 32768
            d3d11_resource_misc_tile_pool = 131072
            d3d11_resource_misc_tiled = 262144
            d3d11_resource_misc_hw_protected = 524288
            d3d11_resource_misc_shared_displayable = 1048576
            d3d11_resource_misc_shared_exclusive_writer = 2097152

        class D3d11ResourceMiscFlags2(Enum):
            dds_alpha_mode_unknown = 0
            dds_alpha_mode_straight = 1
            dds_alpha_mode_premultiplied = 2
            dds_alpha_mode_opaque = 3
            dds_alpha_mode_custom = 4
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dxgi_format = KaitaiStream.resolve_enum(Dds.HeaderDxt10.DxgiFormats, self._io.read_u4le())
            self.d3d10_resource_dimension = KaitaiStream.resolve_enum(Dds.HeaderDxt10.D3d10ResourceDimensionFormats, self._io.read_u4le())
            self.misc_flag = KaitaiStream.resolve_enum(Dds.HeaderDxt10.D3d11ResourceMiscFlags, self._io.read_u4le())
            self.array_size = self._io.read_u4le()
            self.misc_flags2 = KaitaiStream.resolve_enum(Dds.HeaderDxt10.D3d11ResourceMiscFlags2, self._io.read_u4le())


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



    @property
    def fourcc(self):
        if hasattr(self, '_m_fourcc'):
            return self._m_fourcc

        _pos = self._io.pos()
        self._io.seek(84)
        self._m_fourcc = self._io.read_u4le()
        self._io.seek(_pos)
        return getattr(self, '_m_fourcc', None)


