import time
from pathlib import Path
from struct import pack

import numpy
from numpy import ushort
from parsers.dds import Dds
from parsers.tex import Tex

lod_offset = numpy.array([0, 1, 2])


def get_tex_mipmap_length_format(height, width, fourcc):
    # potentially might put in BC4 and BC5 (ATI1, ATI2)
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt1:
        return int(height * width // 2)
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt3 or fourcc == Dds.DdsPixelformat.PixelFormats.dxt5 or fourcc == Dds.DdsPixelformat.PixelFormats.dx10:
        return int(height * width * 2)
    if fourcc == Dds.DdsPixelformat.PixelFormats.none:
        return int(height * width * 4)
    else:
        return None


def get_mipmap_offsets(mipmap_length, mipmap_count):
    offset_array = numpy.zeros(13, dtype=int)
    offset = 80
    j = 0
    try:
        for i in range(mipmap_count):
            offset_array[j] = offset
            offset += mipmap_length
            mipmap_length = max(16, mipmap_length >> 2)
            j += 1
        return offset_array
    except IndexError as e:
        raise SystemExit(
            'Image has too many mipmaps. Mipmap amount: ' + str(mipmap_count) + '. Check last \'given\' image.\nToo '
                                                                                'many mipmaps can be caused by:\n1) '
                                                                                'Having too large an image. '
                                                                                'TEX supports up to 4096x4096 '
                                                                                'resolution *only* if you are using '
                                                                                'mipmaps.\n2) A broken cubemap. Check '
                                                                                'if image ends in \'_e\' or \'_f\'. '
                                                                                'You cannot import cubemaps anyway, '
                                                                                'so get rid of it.\n 3) I don\'t '
                                                                                'know.') from e


def get_tex_offset_array(dds):
    tex_mipmap_length = get_tex_mipmap_length_format(dds.hdr.height, dds.hdr.width, dds.hdr.ddspf.fourcc)
    tex_offset_array = get_mipmap_offsets(tex_mipmap_length, dds.hdr.mipmap_count)
    return tex_offset_array


def get_tex_attribute(dds):
    return Tex.Header.Attribute.texture_type_2d.value


def get_tex_format(dds):
    fourcc = dds.hdr.ddspf.fourcc
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt1:
        return Tex.Header.TextureFormat.dxt1.value
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt3:
        return Tex.Header.TextureFormat.dxt3.value
    if fourcc == Dds.DdsPixelformat.PixelFormats.dxt5:
        return Tex.Header.TextureFormat.dxt5.value
    if fourcc == Dds.DdsPixelformat.PixelFormats.dx10:
        if dds.hdr_dxt10.dxgi_format == Dds.HeaderDxt10.DxgiFormats.dxgi_format_bc7_unorm:
            return Tex.Header.TextureFormat.bc7
    if fourcc == Dds.DdsPixelformat.PixelFormats.none:
        return Tex.Header.TextureFormat.b8g8r8a8.value


def get_tex_height(dds):
    return ushort(dds.hdr.width)


def get_tex_width(dds):
    return ushort(dds.hdr.height)


def get_tex_mip_levels(dds):
    return ushort(dds.hdr.mipmap_count)


def get_tex_depth(dds):
    return ushort(dds.hdr.depth)


def get_tex_binary(path):
    dds_binary = Dds.from_file(path)
    header_info = pack('<IIHHHH', get_tex_attribute(dds_binary), get_tex_format(dds_binary), get_tex_width(dds_binary),
                       get_tex_height(dds_binary), get_tex_depth(dds_binary), get_tex_mip_levels(dds_binary))
    header = (header_info + lod_offset.tobytes() + get_tex_offset_array(dds_binary).tobytes())
    body = (b''.join(dds_binary.bd.data))
    tex_binary = header + body
    return tex_binary


# todo error handling

if __name__ == '__main__':
    p = Path('./images/test/')
    grabber = list(p.glob('**/*.dds'))
    start_time = time.time()

    for dds_path in grabber:
        print('given:' + str(dds_path))
        output_path = Path("./output/" + str((dds_path.with_name(dds_path.stem + '.tex'))))
        binary = get_tex_binary(dds_path)
        print('written:' + str(output_path))
        output_path.parent.mkdir(exist_ok=True, parents=True)
        with open(output_path, 'wb') as wb:
            wb.write(binary)
    execution_time = (time.time() - start_time)
    print("Execution Time: " + str(round(execution_time)) + " sec")
