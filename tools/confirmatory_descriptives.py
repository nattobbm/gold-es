# -*- coding: utf-8 -*-
"""Descriptive supplements to the frozen confirmatory run (2026-08-30).

NOT additional hypothesis tests. Two things only:
  1. two-sided p = 2 x one-sided p (all t > 0), the reporting-convention
     supplement committed on 2026-08-03 (robustness doc / action A1), before
     unblinding;
  2. descriptive context for the confirmatory sample: date range and share of
     days with z > 0, matching what the exploratory report published, so the
     two samples are comparable.

Bucket/z logic replicates analysis_frozen.py exactly; the frozen script itself
is not modified or imported.
"""
import os

import numpy as np
import pandas as pd

REPO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gold-es")
INSTRUMENTS = ["ES", "MES", "GC", "MGC"]
CONFIRM_START = "2026-07-15"
N_DAYS = 30

# one-sided p values as printed by the frozen run (verbatim)
FROZEN_P1S = {"ES": 3.56e-10, "MES": 6.01e-13, "GC": 1.44e-05, "MGC": 2.00e-08,
              "MES-ES": 6.28e-10, "MGC-GC": 1.21e-02}


def daily_bucket_z(df):
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    if df["datetime"].dt.tz is None:
        df["datetime"] = df["datetime"].dt.tz_localize("America/New_York")
    else:
        df["datetime"] = df["datetime"].dt.tz_convert("America/New_York")
    df = df.set_index("datetime").between_time("09:30", "16:00", inclusive="left")
    df["date"] = df.index.date
    df["bucket"] = df.index.floor("15min").strftime("%H:%M")
    rows = []
    for date, g in df.groupby("date"):
        if len(g) < 0.95 * 78:
            continue
        b = g.groupby("bucket")["volume"].sum()
        if len(b) < 26 or b.std(ddof=1) == 0:
            continue
        z = (b - b.mean()) / b.std(ddof=1)
        rows.append({"date": date, "z": z.get("10:15", np.nan)})
    return pd.DataFrame(rows).dropna().sort_values("date")


series = {}
for sym in INSTRUMENTS:
    z = daily_bucket_z(pd.read_csv(os.path.join(REPO, "data", f"{sym}.csv")))
    z = z[z["date"] >= pd.to_datetime(CONFIRM_START).date()].head(N_DAYS)
    series[sym] = z.set_index("date")["z"]

print("=== 1. Two-sided p (supplement, = 2 x one-sided; not the decision rule) ===")
for k, p1 in FROZEN_P1S.items():
    print(f"{k}: p(one-sided)={p1:.2e}  ->  p(two-sided)={2*p1:.2e}")

print("\n=== 2. Confirmatory sample descriptives (not a test) ===")
for sym in INSTRUMENTS:
    s = series[sym]
    print(f"{sym}: N={len(s)}  {s.index.min()} .. {s.index.max()}  "
          f"mean_z={s.mean():+.3f}  median_z={s.median():+.3f}  "
          f"days z>0 = {(s>0).sum()}/{len(s)} ({100*(s>0).mean():.1f}%)")

print("\n=== 3. Exploratory vs confirmatory ===")
EXPLORATORY = {"ES": 0.743, "MES": 1.197, "GC": 1.071, "MGC": 1.245}
for sym in INSTRUMENTS:
    e, c = EXPLORATORY[sym], series[sym].mean()
    print(f"{sym}: exploratory {e:+.3f} -> confirmatory {c:+.3f}  "
          f"(change {c-e:+.3f}, {100*(c-e)/e:+.1f}%)")
EXPL_DIFF = {"MES-ES": 0.45, "MGC-GC": 0.17}
for micro, full in (("MES", "ES"), ("MGC", "GC")):
    k = f"{micro}-{full}"
    c = (series[micro] - series[full]).dropna().mean()
    e = EXPL_DIFF[k]
    print(f"{k}: exploratory {e:+.3f} -> confirmatory {c:+.3f} (change {c-e:+.3f})")
