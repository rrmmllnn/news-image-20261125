#!/usr/bin/env python3
"""Hand out the 25 November 2026 front page.

The picture lives beside this file as entry.png. This script draws
nothing and fetches nothing: it reads that bundled picture, checks
it is one whole 1024 by 1024 PNG under a mebibyte, and writes an
exact copy to the output path, then proves the copy matches. Run it
plain to write the copy, --check to inspect the bundle without
writing anything, or --list to see the stories on the page.
"""

import hashlib
import os
import sys
from pathlib import Path

MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
TAIL = bytes([0, 0, 0, 0]) + b"IEND" + bytes([0xAE, 0x42, 0x60, 0x82])
SIDE = 1024
LIMIT = 1024 * 1024

ITEMS = [
    ("Ukraine's war at sea",
     "Zelenskyy confirms Kyiv's drone strike on the Russian cargo ship "
     "Sparta II in the Gulf of Finland and says Ukraine sank a Russian "
     "warship off Benghazi; Norway urges caution, Putin warns of "
     "retaliation."),
    ("Huawei convicted in US trial",
     "A US jury finds Huawei guilty of trade-secrets conspiracy and "
     "fraud over its Iran business, acquitting it of racketeering."),
    ("Houthis hit Riyadh's tallest tower",
     "A Houthi strike wounds 11 in Riyadh; the Houthis sit 60 km from "
     "Aden, which Yemeni forces say they will not take."),
    ("Sarkozy and Bruni to trial",
     "France orders Nicolas Sarkozy and Carla Bruni to trial over the "
     "Libya case; a first hearing is set for 1 April 2027."),
    ("Kyiv toll reaches 11",
     "Rescuers pull 11 dead from a Kyiv apartment block hit by drones; "
     "leaked Russian records put the war dead at 720,000."),
    ("Nvidia roars back 31.5%",
     "Nvidia gains nearly $1 trillion in a day; Huang, back as CEO, "
     "recoups nearly $34 billion."),
    ("Turkish crash; migrants missing",
     "A Turkish helicopter crashes on a training flight, killing five; "
     "175 migrants are missing after a boat from Senegal vanishes."),
]


def poster():
    """Where the bundled picture sits."""
    return Path(__file__).resolve().parent / "entry.png"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def examine(data):
    """Refuse anything that is not our whole square PNG."""
    if data[:8] != MAGIC:
        raise ValueError("bundled file lacks the PNG magic bytes")
    if len(data) > LIMIT:
        raise ValueError("bundled file is over the 1 MiB limit")
    if data[12:16] != b"IHDR":
        raise ValueError("bundled file's first chunk is not IHDR")
    wide = int.from_bytes(data[16:20], "big")
    tall = int.from_bytes(data[20:24], "big")
    if (wide, tall) != (SIDE, SIDE):
        raise ValueError(f"expected a {SIDE}x{SIDE} image, got {wide}x{tall}")
    if data[-12:] != TAIL:
        raise ValueError("bundled file lacks a proper PNG ending")
    return wide, tall


def show_items():
    for n, (head, body) in enumerate(ITEMS, 1):
        print(f"{n}. {head}")
        print(f"   {body}")


def check_only():
    data = poster().read_bytes()
    wide, tall = examine(data)
    print(f"image: entry.png ({wide}x{tall}, {len(data)} bytes)")
    print(f"sha256: {digest(data)}")
    print("bundle OK: PNG magic, 1024x1024, under 1 MiB, IEND present")
    print()
    show_items()
    return 0


def hand_out(dest):
    data = poster().read_bytes()
    examine(data)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    back = dest.read_bytes()
    if digest(back) != digest(data):
        raise ValueError("copy does not match the bundled picture")
    print(f"wrote {dest} ({len(back)} bytes, sha256 {digest(data)})")
    return 0


def usage():
    print("usage: main.py [--output PATH] [--check] [--list]")
    print("  default output: $MAKEFUN_OUTPUT_DIR/entry.png or /output/entry.png")


def run(argv):
    target = None
    mode = "write"
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--check":
            mode = "check"
        elif arg == "--list":
            mode = "list"
        elif arg == "--help":
            usage()
            return 0
        elif arg == "--output" and i + 1 < len(argv):
            i += 1
            target = Path(argv[i])
        elif arg.startswith("--output="):
            target = Path(arg.split("=", 1)[1])
        else:
            print(f"unknown argument: {arg}", file=sys.stderr)
            usage()
            return 2
        i += 1
    if mode == "check":
        return check_only()
    if mode == "list":
        show_items()
        return 0
    if target is None:
        base = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        target = Path(base) / "entry.png"
    return hand_out(target)


if __name__ == "__main__":
    try:
        sys.exit(run(sys.argv[1:]))
    except (OSError, ValueError) as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)
