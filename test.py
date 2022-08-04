from parsers.dds import Dds
# just tests my parsers
print("hello")
f = Dds.from_file("squidward-256-BGRA_32.dds")
f1 = Dds.from_file("squidward-256-BC1.dds")
print(str(f.hdr.flags) + " BGRA file")
print(str(f1.hdr.flags) + " BC1 file")
