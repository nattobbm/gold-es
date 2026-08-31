# -*- coding: utf-8 -*-
"""Confirmatory-sample readiness check — BAR COUNTS ONLY.

Iron rule 3 permits row-count and date-range checks on confirmatory data.
This script therefore reads ONLY the timestamp column: it counts RTH 5-minute
bars per calendar day and applies the preregistered qualifying-day rule
(>=95% of 78 expected bars, per preregistration section 3).

It does NOT read the volume column, does NOT bucket, and does NOT compute
z-scores or any test statistic. Its sole output is: how many qualifying days
have accrued since 2026-07-15, and the date of the 30th.
"""
import os
import sys

import pandas as pd

ARCHIVE = sys.argv[1] if len(sys.argv) > 1 else None
INSTRUMENTS = ["ES", "MES", "GC", "MGC"]
CONFIRM_START = pd.Timestamp("2026-07-15").date()
N_DAYS = 30
MIN_COV = 0.95
EXPECTED = 78

if ARCHIVE is None:
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "gold-es", "archive")
    ARCHIVE = os.path.join(base, sorted(os.listdir(base))[-1])

print(f"archive: {ARCHIVE}\n")

for sym in INSTRUMENTS:
    path = os.path.join(ARCHIVE, f"{sym}_5m.csv")
    # read ONLY the timestamp column - volume is deliberately not loaded
    df = pd.read_csv(path, usecols=["time"])
    ts = pd.to_datetime(df["time"], utc=True).dt.tz_convert("America/New_York")
    rth = ts[(ts.dt.time >= pd.Timestamp("09:30").time())
             & (ts.dt.time < pd.Timestamp("16:00").time())]
    counts = rth.dt.date.value_counts().sort_index()
    counts = counts[counts.index >= CONFIRM_START]
    qual = counts[counts >= MIN_COV * EXPECTED]
    nonqual = counts[counts < MIN_COV * EXPECTED]

    status = "COMPLETE" if len(qual) >= N_DAYS else "INCOMPLETE"
    line = (f"{sym}: qualifying days since {CONFIRM_START} = {len(qual)} "
            f"({status}; need {N_DAYS})")
    if len(qual) >= N_DAYS:
        line += f"  |  30th qualifying day = {qual.index[N_DAYS-1]}"
    print(line)
    print(f"     days below 95% coverage: "
          f"{[f'{d} ({c} bars)' for d, c in nonqual.items()] or 'none'}")
    print(f"     last date present in archive: {counts.index[-1]}")
