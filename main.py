#!/usr/bin/env python3
"""Entrypoint for news-image-20261123.

Copies the committed entry.png into the output directory, verifying it
against the committed SHA-256. Standard library only. It does NOT render
anything and does NOT call build_image.py.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "dc4711a5ec0bb318a454b056f902b48384b4e744a14c2cb39781c3129c845653"


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    with open(SRC, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print("sha256 mismatch: got %s expected %s" % (digest, EXPECTED_SHA256),
              file=sys.stderr)
        sys.exit(1)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("copied entry.png -> %s" % dst)
    print("sha256 %s" % digest)


if __name__ == "__main__":
    main()
