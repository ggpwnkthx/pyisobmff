# pyisobmff

This is a Python library that implements the ISO/IEC 14496-12:2015 standard, also known as the ISO Base Media File Format (ISOBMFF). This standard specifies the structure and usage of media files that can be used to store timed media information.

The library is structured around the concept of "boxes", which are the basic building blocks of ISOBMFF files. Each box represents a specific piece of data or metadata in the file. The library provides classes for most types of boxes, allowing you to read the data they contain.

The intention of this project is to provide a way to lazy-load only the ISOBMFF box data that you need, and to adaptively seek to and ignore data that you don't needed.

## Usage

You can kind of treat `Scanner` and `Box` objects like lists and dictionaries by using square brackets to select child boxes. When an child is requested by its index number, it will checks its cache first and return the box at that postion. If not, it will scan thee file until that index is found. When an child is requested by a key string, the box will be fully scanned and a `list` of all boxes with a type equal to the requested key will be returned. If only one box is found, that one object will bee returned.

### Basic

```python
import isobmff

# Open the .mp4 file in binary read mode
fh = open("path/to/file.mp4", mode="rb")

# Create an ISOBMFF scanner object to parse the .mp4 file
iso = isobmff.Scanner(fh)

# Iterate over the media tracks in the file
for track in iso["moov"]["trak"]:
    # Check if the track is a video track
    if track["mdia"]["hdlr"].handler_type == "vide":
        # Calculate the aspect ratio of the video
        ratio = track["tkhd"].width / track["tkhd"].height
        # Calculate the duration of the video in seconds
        duration = track["mdia"]["mdhd"].duration / track["mdia"]["mdhd"].timescale
        # Get the number of frames in the video
        frames = track["mdia"]["minf"]["stbl"]["stsz"].sample_count
        # Calculate the frame rate of the video
        fps = frames / duration
        # Get the codec used for the video track
        codec = [
            codec for codec in track["mdia"]["minf"]["stbl"]["stsd"].sample_entries
        ][0].type

        # Print the aspect ratio, duration, frame rate, and codec of the video track
        print((ratio, duration, fps, codec))

    # Check if the track is an audio track
    elif track["mdia"]["hdlr"].handler_type == "soun":
        # Get the sample rate of the audio track
        sample_rate = track["mdia"]["mdhd"].timescale
        # Calculate the duration of the audio in seconds
        duration = track["mdia"]["mdhd"].duration / sample_rate
        # Get the codec used for the audio track
        codec = [
            codec for codec in track["mdia"]["minf"]["stbl"]["stsd"].sample_entries
        ][0].type

        # Print the sample rate, duration, and codec of the audio track
        print((sample_rate, duration, codec))

```

### Crawler

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

# Create a filesystem object for handling files
fs = fsspec.filesystem("http")

# Open the .mp4 file from the URL in binary read mode
fh = fs.open(
    "https://download.samplelib.com/mp4/sample-30s.mp4",
    mode="rb",
)

# Create an ISOBMFF scanner object to parse the .mp4 file
iso = isobmff.Scanner(fh)

# Iterate over the two known track positions
for track in [
    iso[-1][1],
    iso[-1][2],
]:
    # Check the known handler position to determin the track type
    if track[2][1].handler_type == "vide":
        # Print the duration, width, and height of the video track
        print((track[0].duration, track[0].width, track[0].height))
    if track[2][1].handler_type == "soun":
        # Print the duration and volume of the audio track
        print((track[0].duration, track[0].volume))

# The output is:
# (30367, 1920.0, 1080.0)
# (30465, 1.0)
```

## Features

- Provides classes that represent different components of the ISO/IEC 14496-12:2015 standard.
- Lazy loading of ISOBMFF box data as needed.
- Adaptively seeks to and ignores data.
- Includes type hinting for better code readability and static analysis.
- Extendible Box type registry.

### Implemented Box Types

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

### Custom Box Types

To add or overwrite existing Box types, update the `BOX_TYPES` global dictionary accessible from the `isobmff` module. The key should be the 4-byte `type` as a string and the value should be the class to use.

#### Example

```python
import isobmff
import functools

# Define a new class, CustomBox, which inherits from the FullBox class in the isobmff.box module.
class CustomBox(isobmff.box.FullBox):
  # Define a cached property, custom_ID. The @functools.cached_property decorator means that the function's return value will be cached, so it only needs to be computed once.
  @functools.cached_property
  def custom_ID(self) -> int:
    # Calculate the start position of the custom_ID field in the box.
    start = super().header_size
    # If the version of the box is 0, the custom_ID is a 16-bit unsigned integer.
    if self.version == 0:
      return self.slice.subslice(start, start + 2).unpack(">H")[0]
    # If the version of the box is 1, the custom_ID is a 32-bit unsigned integer.
    elif self.version == 1:
      return self.slice.subslice(start, start + 4).unpack(">I")[0]
    # Otherwise, the custom_ID is a 64-bit unsigned integer.
    return self.slice.subslice(start, start + 8).unpack(">I")[0]

  @functools.cached_property
  def duration(self) -> int:
    # Calculate the start position of the duration field in the box, which depends on the version of the box.
    if self.version == 0:
      start = super().header_size + 2
    elif self.version == 1:
      start = super().header_size + 4
    else:
      start = super().header_size + 8
    # The duration is a 64-bit unsigned integer.
    return self.slice.subslice(start, start + 8).unpack(">Q")[0]

  # Define a property, header_size. This is used to determine if there are child boxes and where to find them.
  @property
  def header_size(self) -> int:
    # The size of the header depends on the version of the box.
    if self.version == 0:
      return super().header_size + 2 + 8
    elif self.version == 1:
      return super().header_size + 4 + 8
    return super().header_size + 8 + 8

# Add the CustomBox class to the dictionary of box types in the isobmff module.
isobmff.BOX_TYPES.update({
  "type": CustomBox
})
```

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

This library is designed to provide a high-level interface for working with different file systems. It supports a wide range of file systems, including local file systems, FTP, SFTP, HTTP, HTTPS, Amazon S3, Google Cloud Storage, and Hadoop Distributed File System (HDFS). It's particularly useful when you need to work with large datasets that are stored across multiple file systems.

#### [smart_open](https://github.com/fsspec/filesystem_spec)

This library serves a similar purpose as fsspec but is more focused on providing a simple way to stream large files, whether they're stored locally or in the cloud. It supports local file systems, Amazon S3, Google Cloud Storage, and HTTP/HTTPS.

For files that are accessible strictly via HTTP(S), not S3 or any other wrapping protocol, I would suggest using fsspec.

## Todo

- Implement missing box types.
- Improve error handling for unsupported box types.

## Caveats

- Box types that have not been implemented will have a `type` and `size` but their properties and children will not be parsed.
- AI was used to help generate some of the classes based on the pseudo code in the ISO/IEC 14496-12:2015 documentation. The majority have been manually reviewed and tested, but there are some that have not been tested, yet.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## Authors

- [Isaac Jessup](https://github.com/ggpwnkthx)

## License

This project is licensed under the GPL-3.0-or-later
