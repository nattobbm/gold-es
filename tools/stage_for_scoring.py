# -*- coding: utf-8 -*-
"""Stage confirmatory data into the paths/columns analysis_frozen.py declares.

This is FILE PLACEMENT ONLY, not analysis:
  archive/pull_YYYY-MM-DD/{SYM}_5m.csv  ->  data/{SYM}.csv
  column "time" -> "datetime" (the frozen script's declared input format:
  "CSV files of 5-minute bars per instrument (columns: datetime, volume)")

No rows are filtered, reordered, or altered. The frozen script does its own
RTH filtering, qualifying-day filtering, and .head(30) sample truncation, so
extra data outside the confirmatory window is ignored by the script itself
and no discretion is exercised here.
"""
import os
import shutil
import sys

import pandas as pd

REPO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gold-es")
INSTRUMENTS = ["ES", "MES", "GC", "MGC"]

base = os.path.join(REPO, "archive")
src_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, sorted(os.listdir(base))[-1])
dst_dir = os.path.join(REPO, "data")
os.makedirs(dst_dir, exist_ok=True)

print(f"source archive: {os.path.basename(src_dir)}")
for sym in INSTRUMENTS:
    df = pd.read_csv(os.path.join(src_dir, f"{sym}_5m.csv"))
    df = df.rename(columns={"time": "datetime"})
    out = os.path.join(dst_dir, f"{sym}.csv")
    df.to_csv(out, index=False)
    print(f"  data/{sym}.csv  rows={len(df)}  cols={list(df.columns)}")

print("\nStaged. analysis_frozen.py is now runnable; it has NOT been run.")
