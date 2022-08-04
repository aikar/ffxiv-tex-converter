from parsers.dds import Dds
from parsers.tex import Tex

# just tests my parsers
print("hello")
f = Dds.from_file("images/dds/squidward-256-BGRA_32.dds")
f1 = Dds.from_file("images/dds/squidward-256-BC1.dds")
f_tex = Tex.from_file("images/tex/squidward-256-BGRA_32.tex")
f1_tex = Tex.from_file("images/tex/squidward-256-BC1.tex")

print(str(f1.hdr.ddspf.fourcc))
print(str(f1_tex.hdr.format))


