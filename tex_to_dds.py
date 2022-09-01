import time
from pathlib import Path
from struct import pack
import numpy
from parsers.dds import Dds
from parsers.tex import Tex


def get_dds_height(tex):
    return int(tex.hdr.height)


def get_dds_width(tex):
    return int(tex.hdr.width)


def get_dds_mipmapCount(tex):
    return int(tex.hdr.mip_levels)


def get_dds_fourcc(tex):
    format = tex.hdr.format
    tex_tf = Tex.Header.TextureFormat
    ddspf_pf = Dds.DdsPixelformat.PixelFormats
    if format == tex_tf.dxt1:
        return ddspf_pf.dxt1
    if format == tex_tf.dxt5:
        return ddspf_pf.dxt5
    if format == tex_tf.dxt3:
        return ddspf_pf.dxt3
    if format == tex_tf.bc7:
        return ddspf_pf.dx10
    if format == tex_tf.b8g8r8a8:
        return ddspf_pf.none


def get_pitch(width, fourcc):
    # doc: https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dx-graphics-dds-pguide#dds-file-layout
    ddspf_pf = Dds.DdsPixelformat.PixelFormats
    if fourcc == ddspf_pf.none:
        bits_per_pixel = 32
        pitch = (width * bits_per_pixel + 7) / 8
    else:
        if fourcc == ddspf_pf.dxt1:
            block_size = 8
        else:
            block_size = 16
        pitch = max(1, ((width + 3) / 4)) * block_size
    return int(pitch)


def get_ddspf_header(fourcc):
    ddspf_pf = Dds.DdsPixelformat.PixelFormats
    ddspf_ff = Dds.DdsPixelformat.FormatFlags
    size = 32
    if fourcc != ddspf_pf.none:
        flags = ddspf_ff.ddpf_fourcc.value
        rgbBitCount = 0
        rBitMask = 0
        gBitMask = 0
        bBitmask = 0
        aBitmask = 0
    if fourcc == ddspf_pf.none:
        # basically just BGRA (B,G,R,A) w/ 8bit per channel, eg rbitmask = [0,0,255,0], could write as array but w/e.
        flags = ddspf_ff.ddpf_alpha.value + ddspf_ff.ddpf_rgb.value
        rgbBitCount = 32
        rBitMask = 16711680
        gBitMask = 65280
        bBitmask = 255
        aBitmask = 4278190080

        # no error catching I want this to break if it's fucked up.
    ddspf_header = pack('<IIIIIIII', size, flags, fourcc.value, rgbBitCount, rBitMask, gBitMask, bBitmask, aBitmask)
    return ddspf_header


def get_dds_flags(fourcc, mipmapCount):
    ff = Dds.Header.FormatFlags
    ddspf_pf = Dds.DdsPixelformat.PixelFormats
    flags = (ff.ddsd_caps.value + ff.ddsd_width.value + ff.ddsd_height.value)
    if fourcc == ddspf_pf.none:
        flags += ff.ddsd_pitch.value
    else:
        flags += ff.ddsd_linearsize.value
    if mipmapCount > 1:
        flags += ff.ddsd_mipmapcount.value
    return flags


def get_dds_caps1(tex):
    cf = Dds.Header.CapsFlags
    flags = cf.ddscaps_texture.value
    if tex.hdr.mip_levels > 1:
        flags += (cf.ddscaps_complex.value + cf.ddscaps_mipmap.value)
    return flags


def get_dds_binary(path):
    tex_binary = Tex.from_file(path)
    fourcc = get_dds_fourcc(tex_binary)
    mipmapCount = get_dds_mipmapCount(tex_binary)

    # here comes the structure
    magic = b'DDS '
    size = 124
    flags = get_dds_flags(fourcc, mipmapCount)
    height = get_dds_height(tex_binary)
    width = get_dds_width(tex_binary)
    pitch = get_pitch(width, fourcc)
    # mipmapCount goes here
    depth = 1
    reserved1_array = numpy.zeros(11, dtype=int)
    ddspf_header = get_ddspf_header(fourcc)
    caps1 = get_dds_caps1(tex_binary)
    caps2 = 0
    caps3 = 0
    caps4 = 0
    reserved2 = 0

    header = magic + pack('<IIIIIII', size, flags, height, width, pitch, depth,
                          mipmapCount) + reserved1_array.tobytes() + ddspf_header + pack('<IIIII', caps1, caps2, caps3,
                                                                                         caps4, reserved2)
    body = (b''.join(tex_binary.bdy.data))
    dds_binary = header + body
    return dds_binary


if __name__ == '__main__':
    p = Path('./images/test/')
    grabber = list(p.glob('**/*.tex'))
    start_time = time.time()
    for tex_path in grabber:
        print('given:' + str(tex_path))
        output_path = Path("./output/" + str((tex_path.with_name(tex_path.stem + '.dds'))))
        binary = get_dds_binary(tex_path)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        print('written:' + str(output_path))
        with open(output_path, 'wb') as wb:
            wb.write(binary)
    execution_time = (time.time() - start_time)
    print("Execution Time: " + str(round(execution_time)) + " sec")
