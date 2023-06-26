# pyisobmff

`pyisobmff` is a Python library that implements the ISO/IEC 14496-12:2015 standard, also known as the ISO Base Media File Format (ISOBMFF). This standard specifies the structure and usage of media files that can be used to store timed media information. The intention of this project is to provide a way to lazy load only the ISOBMFF box data that the user needs, and to adaptively seek and ignore data that is not needed.

## Features
- Provides classes that represent different components of the ISO/IEC 14496-12:2015 standard.
- Lazy loading of ISOBMFF box data as needed.
- Adaptively seeks and ignores unneeded data.
- Includes type hinting for better code readability and static analysis.

### Implemented Types
95 Unique Types + 9 Aliases
```
bxml cdsc cinf cprt ctts dref dinf edts elng elst
fdel font ftyp free frma hint hdlr hind iinf idat
iloc infe ipro iref ixml kind mdhd mdia mehd mere
meta mdat mfhd mfra mfro minf moof moov mvex mvhd
nmhd padb pdin pitm prft saio saiz sbgp schi schm
sdp  sdtp skip sinf sidx skcr smhd ssix stbl stco
stdp stsc stsd stsh stss stsz stvi styp stsg stsh
strd strk stri subs subp subp subs subp subp subs
subt tdat tfdt tfhd tfdt tfra tkhd tref tsel trex
trak trgr trun trun trun tsel txtC udta url  urn
vdep vmhd vplx xml
```

## Caveats
- Box types that have not been implemented will have a `type` and `size` but their properties and children will not be parsed.
- AI was used to help generate some of the classes based on the pseudo code in the ISO/IEC 14496-12:2015 documentation. The majority have been manually reviewed and tested, but there are some that have not been tested, yet.

## Installation
As the library is not registered with pip, you can install it with the following pip command:
```
pip install git+https://github.com/ggpwnkthx/pyisobmff
```

### Optional Packages
#### [chardet](https://github.com/chardet/chardet)
This package attempts to detect string encodings and automatically decode them. If this is not installed only UTF-8, UTF-16 BE/LE, and UTF-32 BE/LE encodings are supported. 

Non-standard and/or future standard Base Media formats may require an expanded set of string decoders.

#### [fsspec](https://github.com/fsspec/filesystem_spec)

This package make working with remote files very convenient.

## Usage
### Basic
```python
import isobmff

fh = open("path/to/file.mp4", mode="rb")
iso = isobmff.Scanner(fh)

def crawl(container, indent=0):
 for box in container:
  print("  " * indent + f"{box}")
  if box.has_children:
   crawl(box.children, indent+1)

crawl(iso)

# <FileTypeBox(type=ftyp,start=0,end=32,size=32,has_children=False)>
# <FreeSpaceBox(type=free,start=32,end=40,size=8,has_children=False)>
# <MediaDataBox(type=mdat,start=40,end=21623517,size=21623477,has_children=False)>
# <MovieBox(type=moov,start=21623517,end=21657943,size=34426,has_children=True)>
#   <MovieHeaderBox(type=mvhd,start=21623525,end=21657943,size=108,has_children=False,version=0)>
#   <TrackBox(type=trak,start=21623633,end=43281468,size=15213,has_children=True)>
#  <TrackHeaderBox(type=tkhd,start=21623641,end=21638846,size=92,has_children=False,version=0)>
#  <EditBox(type=edts,start=21623733,end=43262487,size=36,has_children=True)>
#    <EditListBox(type=elst,start=21623741,end=21623769,size=28,has_children=False,version=0)>
#  <MediaBox(type=mdia,start=21623769,end=64886220,size=15077,has_children=True)>
#    <MediaHeaderBox(type=mdhd,start=21623777,end=21638846,size=32,has_children=False,version=0)>
#    <HandlerBox(type=hdlr,start=21623809,end=43262623,size=95,has_children=False,version=0)>
#    ...
```
### Remote
```python
import isobmff
import fsspec

fh = fs.open(
 "https://download.samplelib.com/mp4/sample-30s.mp4",
 mode="rb",
)
iso = isobmff.Scanner(fh)

for track in [
 iso[-1][0][1] 
 iso[-1][0][2]
]:
 if track.type == "vide":
  print((track.duration, track.width, track.height))
 if track.type == "soun":
  print((track.duration, track.volume))

# (1, 30367, 1920.0, 1080.0)
# (2, 30465, 1.0)
```

## Todo
- Implement missing box types.
- Improve error handling for unsupported box types.
- Add more examples to the usage section.
- Explain box type pattern.

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## License
This project is licensed under the terms of the MIT license.
