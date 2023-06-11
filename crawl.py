from isobmff import Iterator, MP4, crawl
from smart_open import open
import logging
# logging.basicConfig(level=logging.DEBUG)

iso = Iterator(
    open(
        "https://download.samplelib.com/mp4/sample-30s.mp4",
        mode="rb",
    ),
    MP4,
)
crawl(iso)
