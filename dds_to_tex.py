from struct import pack
import numpy as numpy
from numpy import ushort
from parsers.dds import Dds
from parsers.tex import Tex

lod_offset = numpy.array([0, 1, 2])


def get_tex_mipmap_length_format(height, width, fourcc):
    # potentially might put in BC4 and BC5 (ATI1, ATI2)
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt1:
        return int(height * width // 2)
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt3 or fourcc == Dds.DdsPixelformat.PixelFormats.dxt5:
        return int(height * width * 2)
    if fourcc == Dds.DdsPixelformat.PixelFormats.none:
        return int(height * width * 4)
    else:
        return None


def get_mipmap_offsets(mipmap_length, mipmap_count):
    offset_array = numpy.zeros(13, dtype=int)
    offset = 80
    j = 0
    for i in range(mipmap_count):
        offset_array[j] = offset
        offset += mipmap_length
        mipmap_length = max(16, mipmap_length >> 2)
        j += 1
    return offset_array


def get_tex_offset_array(dds):
    tex_mipmap_length = get_tex_mipmap_length_format(dds.hdr.height, dds.hdr.width, dds.hdr.ddspf.fourcc)
    tex_offset_array = get_mipmap_offsets(tex_mipmap_length, dds.hdr.mipmap_count)
    return tex_offset_array


def get_tex_attribute(dds):
    dds_fourcc = dds.hdr.ddspf.fourcc
    if dds_fourcc == Dds.DdsPixelformat.PixelFormats.dxt1 or dds_fourcc == Dds.DdsPixelformat.PixelFormats.dxt3 or \
            dds_fourcc == Dds.DdsPixelformat.PixelFormats.dxt5 or dds_fourcc == Dds.DdsPixelformat.PixelFormats.none:
        return Tex.Header.Attribute.texture_type_2d.value


def get_tex_format(dds):
    dds_fourcc = dds.hdr.ddspf.fourcc
    if dds_fourcc == Dds.DdsPixelformat.PixelFormats.dxt1:
        return Tex.Header.TextureFormat.dxt1.value
    if dds_fourcc == Dds.DdsPixelformat.PixelFormats.dxt3:
        return Tex.Header.TextureFormat.dxt3.value
    if dds_fourcc == Dds.DdsPixelformat.PixelFormats.dxt5:
        return Tex.Header.TextureFormat.dxt3.value
    if dds_fourcc == Dds.DdsPixelformat.PixelFormats.none:
        return Tex.Header.TextureFormat.b8g8r8a8.value


def get_tex_height(dds):
    return ushort(dds.hdr.width)


def get_tex_width(dds):
    return ushort(dds.hdr.height)


def get_tex_mip_levels(dds):
    return ushort(dds.hdr.mipmap_count)


def get_tex_depth(dds):
    return ushort(dds.hdr.depth)


# test
f = Dds.from_file("images/dds/squidward-256-BGRA_32.dds")
body = (b''.join(f.bd.data))
header_pt1 = pack("<IIHHHH", get_tex_attribute(f), get_tex_format(f), get_tex_width(f), get_tex_height(f),
                  get_tex_depth(f), get_tex_mip_levels(f))
test = (header_pt1 + lod_offset.tobytes() + get_tex_offset_array(f).tobytes() + body)
with open('output/squidward-256-BGRA_32.tex', 'wb') as f:
    f.write(test)
