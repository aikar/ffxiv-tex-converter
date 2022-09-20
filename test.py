from pathlib import Path

from parsers.dds import Dds
from parsers.tex import Tex

# just tests my parsers

#problem_child = Dds.from_file("images/test/est_e1/evt/e1e1/texture/e1e1_v0_env01_e.dds")
#problem_child = Tex.from_file("images/raen_d.tex")
#problem_child2 = Dds.from_file("images/raen_d.dds")

good_noodle_out = Dds.from_file("output/images/tex_to_dds/squidward-256-BC7.dds")
good_noodle_in = Dds.from_file("images/dds_to_tex/squidward-256-BC7.dds")
print("hello")

p = Path("images/test/est_e1/evt/e1e1/texture/e1e1_v0_env01_e.dds")