#!/usr/bin/env python3
# Copies the repo-held entry.png to $MAKEFUN_OUTPUT_DIR/entry.png,
# byte for byte, after validating it is a real non-empty PNG.
"""news-image-20261120: write the day's news image to the output directory.

The entry image is a 1024x1024 PNG held in this repository (entry.png),
a dense front-page infographic summing up Friday 20 November 2026:
Russia's massive overnight strike on Ukraine hours after the
Trump-Xi-Putin trilateral in Shenzhen, plus 24 more stories across
markets, conflict, tech, and the wider world. This program copies it,
byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only,
no network, no randomness, no clock: two runs write identical bytes.
"""

import os
import shutil
import sys

IMAGE_NAME = "entry.png"

# The 8-byte signature every PNG file starts with.
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, IMAGE_NAME)
    if not os.path.isfile(source):
        sys.stderr.write(f"news-image-20261120: {IMAGE_NAME} not found beside main.py\n")
        return 1
    with open(source, "rb") as f:
        header = f.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        # A text file, an empty file, or a truncated PNG all fail here:
        # none of them starts with the PNG signature.
        sys.stderr.write(
            f"news-image-20261120: {IMAGE_NAME} is not a valid PNG "
            "(missing or wrong magic header, or the file is empty)\n"
        )
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
