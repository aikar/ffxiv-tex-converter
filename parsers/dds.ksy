meta:
  id: dds
  file-extension: dds
  endian: le
instances:
  fourcc:
    pos: 0x54
    type: u4
seq:
  - id: hdr
    type: header
  - id: hdr_dxt10
    type: header_dxt10
    if: fourcc == 0x30315844
  - id: bd
    type: body
    
types:
  header:
    doc-ref: https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dds-header
    seq:
      - id: magic
        contents: 'DDS '
      - id: size
        type: u4
      - id: flags
        type: u4
        enum: format_flags
      - id: height
        type: u4
      - id: width
        type: u4
      - id: pitch_or_linear_size
        type: u4
      - id: depth
        type: u4
      - id: mipmap_count
        type: u4
      - id: reserved1
        size: 44
      - id: ddspf
        type: dds_pixelformat
      - id: caps
        doc: ppl dont actually use this so w/e
        type: u4
        enum: caps_flags
      - id: caps2
        doc: cubemap and volume stuff
        type: u4
        enum: caps2_flags
      - id: caps3
        doc: unused
        size: 4
      - id: caps4
        doc: unused
        size: 4
      - id: reserved2
        size: 4
    enums:
      format_flags:
        0x1: ddsd_caps
        0x2: ddsd_height
        0x4: ddsd_width
        0x8: ddsd_pitch
        0x1000: ddsd_pixelformat
        0x20000: ddsd_mipmapcount
        0x80000: ddsd_linearsize
        0x800000: ddsd_depth
      caps_flags:
        0x8: ddscaps_complex
        0x400000: ddscaps_mipmap
        0x1000: ddscaps_texture
      caps2_flags:
          0x200: ddscaps2_cubemap
          0x400: ddscaps2_cubemap_positivex
          0x800: ddscaps2_cubemap_negativex
          0x1000: ddscaps2_cubemap_positivey
          0x2000: ddscaps2_cubemap_negativey
          0x4000: ddscaps2_cubemap_positivez
          0x8000: ddscaps2_cubemap_negativez
          0x200000: ddscaps2_volume
  dds_pixelformat:
    seq:
      - id: size
        type: u4
      - id: flags
        type: u4
        enum: format_flags
      - id: fourcc
        type: u4
        enum: pixel_formats
      - id: rgb_bit_count
        type: u4
      - id: r_bit_mask
        # i think bitmasks are easier to understand as arrays
        size: 4
      - id: g_bit_mask
        size: 4
      - id: b_bit_mask
        size: 4
      - id: a_bit_mask
        size: 4
    enums:
      pixel_formats:
        0: none
        0x31545844: dxt1
        0x33545844: dxt3
        0x35545844: dxt5
        0x30315844: dx10
      format_flags:
        0x000001: ddpf_alphapixels
        0x000002: ddpf_alpha
        0x000004: ddpf_fourcc
        0x000040: ddpf_rgb
        0x000200: ddpf_yuv
        0x020000: ddpf_luminance
  header_dxt10:
    seq:
    - id: dxgi_format
      type: u4
      enum: dxgi_formats
    - id: d3d10_resource_dimension
      type: u4
      enum: d3d10_resource_dimension_formats
    - id: misc_flag
      type: u4
      enum: d3d11_resource_misc_flags
    - id: array_size
      type: u4
    - id: misc_flags2
      type: u4
      enum: d3d11_resource_misc_flags2
    enums:
      dxgi_formats:
        0: dxgi_format_unknown
        1: dxgi_format_r32g32b32a32_typeless
        2: dxgi_format_r32g32b32a32_float
        3: dxgi_format_r32g32b32a32_uint
        4: dxgi_format_r32g32b32a32_sint
        5: dxgi_format_r32g32b32_typeless
        6: dxgi_format_r32g32b32_float
        7: dxgi_format_r32g32b32_uint
        8: dxgi_format_r32g32b32_sint
        9: dxgi_format_r16g16b16a16_typeless
        10: dxgi_format_r16g16b16a16_float
        11: dxgi_format_r16g16b16a16_unorm
        12: dxgi_format_r16g16b16a16_uint
        13: dxgi_format_r16g16b16a16_snorm
        14: dxgi_format_r16g16b16a16_sint
        15: dxgi_format_r32g32_typeless
        16: dxgi_format_r32g32_float
        17: dxgi_format_r32g32_uint
        18: dxgi_format_r32g32_sint
        19: dxgi_format_r32g8x24_typeless
        20: dxgi_format_d32_float_s8x24_uint
        21: dxgi_format_r32_float_x8x24_typeless
        22: dxgi_format_x32_typeless_g8x24_uint
        23: dxgi_format_r10g10b10a2_typeless
        24: dxgi_format_r10g10b10a2_unorm
        25: dxgi_format_r10g10b10a2_uint
        26: dxgi_format_r11g11b10_float
        27: dxgi_format_r8g8b8a8_typeless
        28: dxgi_format_r8g8b8a8_unorm
        29: dxgi_format_r8g8b8a8_unorm_srgb
        30: dxgi_format_r8g8b8a8_uint
        31: dxgi_format_r8g8b8a8_snorm
        32: dxgi_format_r8g8b8a8_sint
        33: dxgi_format_r16g16_typeless
        34: dxgi_format_r16g16_float
        35: dxgi_format_r16g16_unorm
        36: dxgi_format_r16g16_uint
        37: dxgi_format_r16g16_snorm
        38: dxgi_format_r16g16_sint
        39: dxgi_format_r32_typeless
        40: dxgi_format_d32_float
        41: dxgi_format_r32_float
        42: dxgi_format_r32_uint
        43: dxgi_format_r32_sint
        44: dxgi_format_r24g8_typeless
        45: dxgi_format_d24_unorm_s8_uint
        46: dxgi_format_r24_unorm_x8_typeless
        47: dxgi_format_x24_typeless_g8_uint
        48: dxgi_format_r8g8_typeless
        49: dxgi_format_r8g8_unorm
        50: dxgi_format_r8g8_uint
        51: dxgi_format_r8g8_snorm
        52: dxgi_format_r8g8_sint
        53: dxgi_format_r16_typeless
        54: dxgi_format_r16_float
        55: dxgi_format_d16_unorm
        56: dxgi_format_r16_unorm
        57: dxgi_format_r16_uint
        58: dxgi_format_r16_snorm
        59: dxgi_format_r16_sint
        60: dxgi_format_r8_typeless
        61: dxgi_format_r8_unorm
        62: dxgi_format_r8_uint
        63: dxgi_format_r8_snorm
        64: dxgi_format_r8_sint
        65: dxgi_format_a8_unorm
        66: dxgi_format_r1_unorm
        67: dxgi_format_r9g9b9e5_sharedexp
        68: dxgi_format_r8g8_b8g8_unorm
        69: dxgi_format_g8r8_g8b8_unorm
        70: dxgi_format_bc1_typeless
        71: dxgi_format_bc1_unorm
        72: dxgi_format_bc1_unorm_srgb
        73: dxgi_format_bc2_typeless
        74: dxgi_format_bc2_unorm
        75: dxgi_format_bc2_unorm_srgb
        76: dxgi_format_bc3_typeless
        77: dxgi_format_bc3_unorm
        78: dxgi_format_bc3_unorm_srgb
        79: dxgi_format_bc4_typeless
        80: dxgi_format_bc4_unorm
        81: dxgi_format_bc4_snorm
        82: dxgi_format_bc5_typeless
        83: dxgi_format_bc5_unorm
        84: dxgi_format_bc5_snorm
        85: dxgi_format_b5g6r5_unorm
        86: dxgi_format_b5g5r5a1_unorm
        87: dxgi_format_b8g8r8a8_unorm
        88: dxgi_format_b8g8r8x8_unorm
        89: dxgi_format_r10g10b10_xr_bias_a2_unorm
        90: dxgi_format_b8g8r8a8_typeless
        91: dxgi_format_b8g8r8a8_unorm_srgb
        92: dxgi_format_b8g8r8x8_typeless
        93: dxgi_format_b8g8r8x8_unorm_srgb
        94: dxgi_format_bc6h_typeless
        95: dxgi_format_bc6h_uf16
        96: dxgi_format_bc6h_sf16
        97: dxgi_format_bc7_typeless
        98: dxgi_format_bc7_unorm
        99: dxgi_format_bc7_unorm_srgb
        100: dxgi_format_ayuv
        101: dxgi_format_y410
        102: dxgi_format_y416
        103: dxgi_format_nv12
        104: dxgi_format_p010
        105: dxgi_format_p016
        106: dxgi_format_420_opaque
        107: dxgi_format_yuy2
        108: dxgi_format_y210
        109: dxgi_format_y216
        110: dxgi_format_nv11
        111: dxgi_format_ai44
        112: dxgi_format_ia44
        113: dxgi_format_p8
        114: dxgi_format_a8p8
        115: dxgi_format_b4g4r4a4_unorm
        
        130: dxgi_format_p208
        131: dxgi_format_v208
        132: dxgi_format_v408
        
        
        189: dxgi_format_sampler_feedback_min_mip_opaque
        190: dxgi_format_sampler_feedback_mip_region_used_opaque
        
        
        0xffffffff: dxgi_format_force_uint
      d3d10_resource_dimension_formats:
        0: d3d10_resource_dimension_unknown
        1: d3d10_resource_dimension_buffer
        2: d3d10_resource_dimension_texture1d
        3: d3d10_resource_dimension_texture2d
        4: d3d10_resource_dimension_texture3d
      d3d11_resource_misc_flags:
        0x1: d3d11_resource_misc_generate_mips
        0x2: d3d11_resource_misc_shared
        0x4: d3d11_resource_misc_texturecube
        0x10: d3d11_resource_misc_drawindirect_args
        0x20: d3d11_resource_misc_buffer_allow_raw_views
        0x40: d3d11_resource_misc_buffer_structured
        0x80: d3d11_resource_misc_resource_clamp
        0x100: d3d11_resource_misc_shared_keyedmutex
        0x200: d3d11_resource_misc_gdi_compatible
        0x800: d3d11_resource_misc_shared_nthandle
        0x1000: d3d11_resource_misc_restricted_content
        0x2000: d3d11_resource_misc_restrict_shared_resource
        0x4000: d3d11_resource_misc_restrict_shared_resource_driver
        0x8000: d3d11_resource_misc_guarded
        0x20000: d3d11_resource_misc_tile_pool
        0x40000: d3d11_resource_misc_tiled
        0x80000: d3d11_resource_misc_hw_protected
        0x100000: d3d11_resource_misc_shared_displayable
        0x200000: d3d11_resource_misc_shared_exclusive_writer
      d3d11_resource_misc_flags2:
        0x0: dds_alpha_mode_unknown
        0x1: dds_alpha_mode_straight
        0x2: dds_alpha_mode_premultiplied
        0x3: dds_alpha_mode_opaque
        0x4: dds_alpha_mode_custom
  body:
    seq:
    - id: data
      size: 4
      repeat: eos

