## tex_body_repair.py

Reads a pair of DDS, TEX; where DDS body replaces TEX body, to repair botched TexTools write.

DDS, TEX must be in images/tex-body-shop folder as such:

    images/tex-body-shop/bar.dds
    images/tex-body-shop/bar.tex

This will then write to:

    output/images/tex-body-shop/bar.tex

* Accepts nested directory structures.
* Is super rudemintary but gets the job done.

---

## test.py

just tests my parsers

---

# parsers

### dds.ksy

* kaitai struct to read dds header, body. body reading is only rudimentary to reach EOF.
* Read [Microsoft DDS_Header Docs](https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dds-header) for more info.

### dds.py

* kaitai generated parser of dds for python. I did have to modify some Enum to be IntFlag instead, as the compiler did
  not do that for me. Just an FYI if you re-compile the dds.ksy for python you might have to redo that.
* Read [Microsoft DDS_Header Docs](https://docs.microsoft.com/en-us/windows/win32/direct3ddds/dds-header) for more info.

