meta:
  id: dds
  file-extension: dds
  endian: le
seq:
  - id: hdr
    type: header
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
        0x10000: ddsd_pixelformat
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
        type: format_flags
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
        
  body:
    seq:
    - id: data
      size: 4
      repeat: eos
    
