## dds_to_tex.py
Converts DDS to TEX.

DDS must be in images/test folder as such:
    
    images/test/bar.dds
    images/test/kitten/foo.dds

This will write to:

    output/images/test/bar.tex
    output/images/test/kitten/bar.tex

* Accepts nested directory structures.
* Does not support DXT10 headers (soon).
* Supports BGRA, BGRX, BC1 (DXT1), BC2 (DXT3), and BC3 (DXT5). 

### Why should I use this over TexTools?
* TexTools breaks mipmaps. Either by falsely calculating the offset, or just erasing the end of the file.
* TexTools doesn't support writing many files at once.
* Textools can't interact with most game textures. TexTools only interacts with character and housing textures.

### When should I use TexTools Texture Importer?
* If mipmaps don't bother you, go ahead.
* If you want to write directly to the game files. Please don't.
* If you are working on a file, and you want to immediately see results.

I personally still use TexTools for a lot of stuff. Please don't perpetuate cultish behavior around mod tools. It's weird.

---

## tex_body_repair.py

Reads a pair of DDS, TEX; where DDS body replaces TEX body, to repair botched TexTools write.

DDS, TEX must be in images/tex-body-shop folder as such:

    images/tex-body-shop/bar.dds
    images/tex-body-shop/bar.tex

This will then write to:

    output/images/tex-body-shop/bar.tex

* Accepts nested directory structures.
* Is super rudimentary but gets the job done.

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

### tex.ksy

* kaitai struct to read tex header, body. body reading is only rudimentary to reach EOF.
* See Penumbra/TexTools/Lumina source code for more info.

### tex.py

*same as the dds.py info really.
