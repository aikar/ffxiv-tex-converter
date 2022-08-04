from parsers.dds import Dds
from parsers.tex import Tex

# just tests my parsers
print("hello")
f0_tex = Tex.from_file("images/tex/squidward-256-BC1_out.tex")
f1_tex = Tex.from_file("images/tex/squidward-256-BC1.tex")
f2_tex = Tex.from_file("images/tex/squidward-256-BC1.tex")

# todo get info for header
# todo write tex mipmap offsets

for offset in f1_tex.hdr.offset_to_surface13:
    print(offset)
for offset in f0_tex.hdr.offset_to_surface13:
    print(offset)

