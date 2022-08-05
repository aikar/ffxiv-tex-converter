from pathlib import Path

from parsers.dds import Dds
from parsers.tex import Tex

# just tests my parsers

problem_child = Dds.from_file("images/test/est_e1/evt/e1e1/texture/e1e1_v0_env01_e.dds")

print("hello")

p = Path("images/test/est_e1/evt/e1e1/texture/e1e1_v0_env01_e.dds")