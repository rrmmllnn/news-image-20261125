#!/usr/bin/env python3
"""Copy the bundled entry.png to the output path (stdlib only).

Usage:
  python3 main.py [--output PATH]   copy entry.png (default /output/entry.png)
  python3 main.py --check           verify the bundled PNG and print its facts
  python3 main.py --list            list the files this entry ships
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
LIMIT = 1048576


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def facts(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG")
    if data[12:16] != b"IHDR":
        raise SystemExit("no IHDR")
    w, h = struct.unpack(">II", data[16:24])
    if data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        raise SystemExit("no IEND")
    return w, h, len(data)


def check():
    w, h, size = facts(SRC)
    print("entry.png: %dx%d, %d bytes, sha256 %s" % (w, h, size, sha256(SRC)))
    if (w, h) != (1024, 1024):
        raise SystemExit("must be 1024x1024")
    if size >= LIMIT:
        raise SystemExit("must be under 1 MiB")
    print("check ok")


def main(argv):
    if "--list" in argv:
        print("entry.png\nmain.py\nREADME.md\nLICENSE")
        return 0
    if "--check" in argv:
        check()
        return 0
    out = "/output/entry.png"
    if "--output" in argv:
        out = argv[argv.index("--output") + 1]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(SRC, "rb") as src, open(out, "wb") as dst:
        dst.write(src.read())
    print("wrote %s sha256 %s" % (out, sha256(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
