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

# todo get info for header
# todo write tex mipmap offsets

for offset in f1_tex.hdr.offset_to_surface13:
    print(offset)

mipmaplength = int(f1_tex.hdr.height * f1_tex.hdr.width/2)
offset = 80
mipmaplengthsum = 0
count = 1
for i in range(f1_tex.hdr.mip_levels):
    print(offset)
    offset += mipmaplength
    mipmaplengthsum += mipmaplength
    mipmaplength = max(16, mipmaplength >> 2)
    count += 1
for i in range(13 - f1_tex.hdr.mip_levels):
    print(0)
    count += 1
