#!/usr/bin/env python3
"""Emit the 20 November 2026 front page.

The repository holds the finished infographic as entry.png: a dense
one-page newspaper summary of Friday 20 November 2026, led by Russia's
overnight strike on Ukraine and followed by 24 further stories. This
script's only job is to place an exact copy of that image at
$MAKEFUN_OUTPUT_DIR/entry.png.

It uses nothing but the standard library, touches no network, reads no
clock, and makes no random choices, so repeated runs produce identical
bytes. Before copying it checks the first eight bytes against the PNG
signature, and refuses to write anything if the image is absent, empty,
or not a PNG at all.
"""

import os
import sys

IMAGE = "entry.png"
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def die(reason):
    """Report a problem on stderr and stop with a nonzero status."""
    sys.stderr.write("news-image-20261120: " + reason + "\n")
    raise SystemExit(1)


def load_image():
    """Return the repository image's bytes, after checking it is a PNG.

    The whole file is read and its opening bytes compared to the PNG
    signature, so a text file, an empty file, or a truncated image is
    caught before anything is written to the output directory.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, IMAGE)
    if not os.path.isfile(path):
        die(IMAGE + " not found beside main.py")
    with open(path, "rb") as handle:
        data = handle.read()
    if len(data) < len(SIGNATURE) or data[: len(SIGNATURE)] != SIGNATURE:
        die(
            IMAGE
            + " is not a valid PNG "
            + "(missing or wrong magic header, or the file is empty)"
        )
    return data


def main():
    """Copy the validated image into the output directory."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if not out_dir:
        die("MAKEFUN_OUTPUT_DIR is not set")
    data = load_image()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, IMAGE)
    with open(target, "wb") as handle:
        handle.write(data)


if __name__ == "__main__":
    main()
