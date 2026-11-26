#!/usr/bin/env python3
"""Ship the finished poster: place a copy in the grader's output folder.

Only the standard library is used. The artwork itself is painted by
draw_timeline.py and travels in this repo as entry.png; all this script
does is drop an exact duplicate at /output/entry.png, or wherever
$MAKEFUN_OUTPUT_DIR points.
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
DEST = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DEST, exist_ok=True)
shutil.copyfile(os.path.join(BASE, "entry.png"),
                os.path.join(DEST, "entry.png"))
