import gc
import os
import time
from multiprocessing import Pool
from pathlib import Path
from struct import pack

import numpy
from tqdm import tqdm

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


def get_dds_dxt10_header(tex):
    dxgi_format = get_dds_dxt10_dxgi_format(tex.hdr.format)
    resource_dimension = get_dds_dxt10_resource_dimension()
    misc_flag = get_dds_dxt10_misc_flag()
    array_size = get_dds_dxt10_array_size()
    misc_flag2 = get_dds_dxt10_misc_flags2()
    dxt10_header = pack('<IIIII', dxgi_format.value, resource_dimension, misc_flag, array_size, misc_flag2)
    return dxt10_header


def get_dds_dxt10_dxgi_format(tex_format):
    tex_tf = Tex.Header.TextureFormat
    dxgi_format = Dds.HeaderDxt10.DxgiFormats
    # todo theoretically should have support for more options but w/e
    # todo could also be rolled into the fourcc
    if tex_format == tex_tf.bc7:
        return dxgi_format.dxgi_format_bc7_unorm


def get_dds_dxt10_resource_dimension():
    # todo for sure
    return 3


def get_dds_dxt10_misc_flag():
    # todo for sure
    return 0


def get_dds_dxt10_array_size():
    return 1


def get_dds_dxt10_misc_flags2():
    # todo for sure
    return 1


def get_pitch(height, width, fourcc):
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
        # microsoft recommends width+3 and height+3, but I just set mine to match nvidia texture tools
        pitch = max(1, ((width) / 4)) * max(1, ((height) / 4)) * block_size
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
    flags = (ff.ddsd_caps.value + ff.ddsd_width.value + ff.ddsd_height.value + ff.ddsd_pixelformat)
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
    ddspf_pf = Dds.DdsPixelformat.PixelFormats

    # here comes the structure
    magic = b'DDS '
    size = 124
    flags = get_dds_flags(fourcc, mipmapCount)
    height = get_dds_height(tex_binary)
    width = get_dds_width(tex_binary)
    pitch = get_pitch(height, width, fourcc)
    # mipmapCount goes here
    depth = 1
    reserved1_array = numpy.zeros(11, dtype=numpy.int32)
    # reserved1_array = b'\x00' * 44
    ddspf_header = get_ddspf_header(fourcc)
    caps1 = get_dds_caps1(tex_binary)
    caps2 = 0
    caps3 = 0
    caps4 = 0
    reserved2 = 0
    header = magic + pack('<IIIIIII', size, flags, height, width, pitch, depth, mipmapCount) + \
             reserved1_array.tobytes() + ddspf_header + pack('<IIIII', caps1, caps2, caps3, caps4, reserved2)
    # if we are dxt10, write dxt10 header
    if fourcc == ddspf_pf.dx10:
        dds_dxt10_header = get_dds_dxt10_header(tex_binary)
        header += dds_dxt10_header

    body = (b''.join(tex_binary.bdy.data))
    dds_binary = header + body

    del tex_binary
    gc.collect()

    return dds_binary


def do_the_thing(input_path):
    # print('given:' + str(input_path))
    output_path = Path('./output') / str((input_path.with_name(input_path.stem + '.dds')))
    output_path.parent.mkdir(exist_ok=True, parents=True)
    binary = get_dds_binary(input_path)
    with open(output_path, 'wb') as wb:
        wb.write(binary)
    del binary
    gc.collect()
    # print('written:' + str(output_path))


def chunks(arr, size):
    """
    split an array into chunks
    :param arr: the array
    :param size: size of each chunk
    :return: yields one chunk of size `size` of `arr`
    """
    for i in range(0, len(arr), size):
        yield arr[i: i + size]


if __name__ == '__main__':
    p = Path('./images/tex_to_dds')
    grabber = list(p.glob('**/*.tex'))
    print(f'Processing {len(grabber)} files.')
    start_time = time.time()

    parallel = True
    if parallel:
        core_count = os.cpu_count()
        # tqdm provides a pretty progress bar
        with tqdm(total=len(grabber), unit="files") as pb:
            # core_count * 32 seemed like a good number
            # if stuff gets slow, lower 32 down to like 24 or something idk.
            # looping in chunks rather than using the pool directly forces python to clean up its subprocesses and
            # prevents overflowing memory to disk
            for chunk in chunks(grabber, core_count):
                with Pool(core_count) as p:
                    p.map(do_the_thing, chunk)
                pb.update(len(chunk))
    else:
        for file in grabber:
            do_the_thing(file)

    execution_time = (time.time() - start_time)
    print("Execution Time: " + str(round(execution_time)) + " sec")
