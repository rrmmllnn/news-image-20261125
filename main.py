#!/usr/bin/env python3
"""Entry point: copy the poster beside this file to the output directory.

Standard library only. The poster itself is drawn by draw_timeline.py and
shipped in this repository as entry.png; this program just places a
byte-identical copy at /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
