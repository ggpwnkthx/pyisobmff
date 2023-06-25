import isobmff
import fsspec
import logging

print(len(isobmff.BOX_TYPES))

fs = fsspec.filesystem('http')

# logging.basicConfig(level=logging.DEBUG)
fh = fs.open(
    "https://download.samplelib.com/mp4/sample-30s.mp4",
    mode="rb",
)
iso = isobmff.Scanner(fh)

def crawl(container, indent=0):
    for box in container:
        print("  " * indent + f"{box}")
        if box.has_children:
            crawl(box.children, indent+1)
    
crawl(iso)
# box = iso[-1][1][1][1][2]
# print(box.slice.read(box.header_size, box.header_size + 4))
