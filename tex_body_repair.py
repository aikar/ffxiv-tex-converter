from pathlib import Path

"""Reads a pair of DDS, TEX; where DDS body replaces TEX body, to repair botched TexTools write.

DDS, TEX must be in images/tex-body-shop folder as such:
images/tex-body-shop/bar.dds
images/tex-body-shop/bar.tex
This will then write to:
output/images/tex-body-shop/bar.tex
Accepts nested directory structures.

"""


def read_byte_to_array(file, length=None):
    try:
        with open(file, "rb") as f:
            barr = bytearray()
            if length is None:
                barr += f.read()
            else:
                barr += f.read(length)
        return barr
    except IOError:
        pass


def byte_body_swap(head_array, body_array):
    if dds_detect(head_array):
        # dds head onto tex body, for debugging
        body = body_array[80:]
        header = head_array[:128]
        out = header + body
    else:
        # tex head onto dds body
        body = body_array[128:]
        header = head_array[:80]
        out = header + body
    return out


def do_thing(head_path, body_path):
    head_array = read_byte_to_array(head_path)
    body_array = read_byte_to_array(body_path)
    output = Path("./output/" + str(head_path))
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        out_array = byte_body_swap(head_array, body_array)
        with open(output, 'wb') as wb:
            wb.write(out_array)
    except TypeError:
        print("missing " + str(head_path.stem))


def dds_detect(array):
    # does this really need to be a function?
    dds_magic = b'DDS '
    return array[:4] == dds_magic


if __name__ == '__tex_body_repair__':

    p = Path('./images/tex-body-shop')  # could make this an argument
    grabber = list(p.glob('**/*.tex'))
    for tex_file in grabber:
        print(tex_file)
        dds_file = (tex_file.with_name(tex_file.stem + ".dds"))
        do_thing(tex_file, dds_file)
