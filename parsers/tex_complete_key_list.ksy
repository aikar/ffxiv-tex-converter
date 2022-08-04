meta:
  id: tex
  file-extension: tex
  endian: le
seq:
  - id: hdr
    type: header
  - id: bdy
    type: body

types:
  header:
    seq:
      - id: type
        type: u4
        enum: attribute
      - id: format
        type: u4
        enum: texture_format
      - id: width
        type: u2
      - id: height
        type: u2
      - id: depth
        type: u2
      - id: mip_levels
        type: u2
      - id: lod_offset3
        doc: 'is always u4[1]=0, u4[2]=1, u4[3]=2'
        # could probably write some verification here, but w/e
        type: u4
        repeat: expr
        repeat-expr: 3
      - id: offset_to_surface13
        doc: 'starts with 0x50, mipmaps offset, so ffxiv knows where to look for each mipmap. offset varies by mipmap1 width and length, and whether compressed or not.'
        type: u4
        repeat: expr
        repeat-expr: 13
    enums:
      attribute:
        0x1: discard_per_frame
        0x2: discard_per_map
        0x4: managed
        0x8: user_managed
        0x10: cpu_read
        0x20: location_main
        0x40: no_gpu_read
        0x80: aligned_size
        0x100: edge_culling
        0x200: location_onion
        0x400: read_write
        0x800: immutable
        0x100000: texture_render_target
        0x200000: texture_depth_stencil
        0x400000: texture_type_1d
        0x800000: texture_type_2d
        0x1000000: texture_type_3d
        0x2000000: texture_type_cube
        0x3C00000: texture_type_mask
        0x4000000: texture_swizzle
        0x8000000: texture_no_tiled
        0x80000000: texture_no_swizzle
      texture_format:
            # might have to remove some of the duplicates. i.e. bc1 and dxt1 both are 0x3420
            0xC: type_shift
            0xF000: type_mask
            0x8: component_shift
            0xF00: component_mask
            0x4: bpp_shift
            0xF0: bpp_mask
            0x0: enum_shift
            0xF: enum_mask
            0x1: type_integer
            0x2: type_float
            0x3: type_dxt
            0x3: type_bc123
            0x4: type_depth_stencil
            0x5: type_special
            0x6: type_bc57
            
            0x0: unknown
            
            # integer types
            0x1130: l8
            0x1131: a8
            0x1440: b4_g4_r4_a4
            0x1441: b5_g5_r5_a1
            0x1450: b8_g8_r8_a8
            0x1451: b8_g8_r8_x8
            
            # floating point types
            0x2150: r32_f
            0x2250: r16_g16_f
            0x2260: r32_g32_f
            0x2460: r16g_16_b16_a16_f
            0x2470: r32_g32_b32_a32_f
            
            # block compression types (dx9)
            0x3420: dxt1
            0x3430: dxt3
            0x3431: dxt5
            0x6230: ati2
            
            # block compression types (dx11)
            0x3420: bc1
            0x3430: bc2
            0x3431: bc3
            0x6230: bc5
            0x6432: bc7
            
            # depth stencil
            0x4140: d16
            0x4250: d24_s8
            
            #special types
            0x5100: null1
            0x5140: shadow16
            0x5150: shadow24
  body:
    seq:
    - id: data
      size: 4
      repeat: eos