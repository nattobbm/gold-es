# -*- coding: utf-8 -*-
"""Phase-2 robustness checks on the EXPLORATORY sample only (dates <= 2026-07-14).

Produces the numbers reported in robustness_exploratory.md (run 2026-08-02).

Bucket/z definition copied verbatim in logic from analysis_frozen.py
(RTH 09:30-16:00 ET, 26 x 15-min buckets, per-day z, >=95% of 78 bars).
analysis_frozen.py itself is NOT touched or imported.

Input: the exploratory {SYM}_5m.csv files at the repo root
(columns: time, open, high, low, close, volume).

Checks:
  A. Baseline reproduction (per instrument: N, mean z, t, one-sided p, %days z>0)
  B. Bonferroni x26 (bucket was chosen post hoc among 26)
  C. First-half / second-half split stability
  D. Weekday effect (incl. Wednesday-vs-rest, EIA recheck)
  E. Holiday / half-day sensitivity (explicitly drop known half-days & adjacent days)
"""
import os

import numpy as np
import pandas as pd
from scipy import stats

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTRUMENTS = ["ES", "MES", "GC", "MGC"]
EXPLORATORY_END = pd.Timestamp("2026-07-14").date()
RTH_START, RTH_END = "09:30", "16:00"
TARGET = "10:15"
MIN_COV = 0.95
EXPECTED = 78

# CME 2026 holidays / early closes inside the sample window (May 4 - Jul 14):
# 2026-05-25 Memorial Day (early close), 2026-06-19 Juneteenth (early close),
# 2026-07-03 Independence Day observed (early close / closed).
SPECIAL = {pd.Timestamp("2026-05-25").date(),
           pd.Timestamp("2026-06-19").date(),
           pd.Timestamp("2026-07-03").date()}
# adjacent regular days (day before / after each special day) for the stricter variant
ADJACENT = {pd.Timestamp("2026-05-22").date(), pd.Timestamp("2026-05-26").date(),
            pd.Timestamp("2026-06-18").date(), pd.Timestamp("2026-06-22").date(),
            pd.Timestamp("2026-07-02").date(), pd.Timestamp("2026-07-06").date()}


def daily_bucket_z(df):
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert("America/New_York")
    df = df.set_index("datetime").between_time(RTH_START, RTH_END, inclusive="left")
    df["date"] = df.index.date
    df["bucket"] = df.index.floor("15min").strftime("%H:%M")
    rows = []
    for date, g in df.groupby("date"):
        if date > EXPLORATORY_END:
            continue
        if len(g) < MIN_COV * EXPECTED:
            continue
        b = g.groupby("bucket")["volume"].sum()
        if len(b) < 26 or b.std(ddof=1) == 0:
            continue
        z = (b - b.mean()) / b.std(ddof=1)
        rows.append({"date": date, "z": z.get(TARGET, np.nan)})
    return pd.DataFrame(rows).dropna().sort_values("date").reset_index(drop=True)


def one_sided_p(s):
    t, p2 = stats.ttest_1samp(s, 0.0)
    return t, (p2 / 2 if t > 0 else 1 - p2 / 2)


series = {}
for sym in INSTRUMENTS:
    df = pd.read_csv(os.path.join(DATA_DIR, f"{sym}_5m.csv"))
    z = daily_bucket_z(df)
    series[sym] = z

print("=== A. Baseline (exploratory sample, frozen method) ===")
for sym in INSTRUMENTS:
    z = series[sym]
    t, p = one_sided_p(z["z"])
    print(f"{sym}: N={len(z)} range={z['date'].min()}..{z['date'].max()} "
          f"mean_z={z['z'].mean():+.3f} t={t:.2f} p1s={p:.2e} "
          f"pct_z_gt0={100*(z['z']>0).mean():.1f}%")

print("\n=== B. Bonferroni x26 (post-hoc bucket selection) ===")
for sym in INSTRUMENTS:
    z = series[sym]
    t, p = one_sided_p(z["z"])
    p26 = min(1.0, p * 26)
    p104 = min(1.0, p * 26 * 4)
    print(f"{sym}: p1s={p:.2e}  p_x26={p26:.2e} ({'sig' if p26 < 0.05 else 'NOT sig'} at 0.05)  "
          f"p_x104={p104:.2e} ({'sig' if p104 < 0.05 else 'NOT sig'})")

print("\n=== C. Split-half stability (chronological halves) ===")
for sym in INSTRUMENTS:
    z = series[sym]["z"]
    n = len(z); h = n // 2
    a, b = z.iloc[:h], z.iloc[h:]
    ta, pa = one_sided_p(a); tb, pb = one_sided_p(b)
    t2, p2 = stats.ttest_ind(a, b, equal_var=False)
    print(f"{sym}: H1 N={len(a)} mean={a.mean():+.3f} p1s={pa:.2e} | "
          f"H2 N={len(b)} mean={b.mean():+.3f} p1s={pb:.2e} | "
          f"halves-differ p(two-sided)={p2:.3f}")

print("\n=== D. Weekday effect ===")
for sym in INSTRUMENTS:
    z = series[sym].copy()
    z["wd"] = pd.to_datetime(z["date"]).dt.day_name()
    parts = []
    for wd in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        s = z.loc[z["wd"] == wd, "z"]
        parts.append(f"{wd[:3]} {s.mean():+.2f}(n={len(s)})")
    groups = [g["z"].values for _, g in z.groupby("wd")]
    F, pA = stats.f_oneway(*groups)
    wed = z.loc[z["wd"] == "Wednesday", "z"]; rest = z.loc[z["wd"] != "Wednesday", "z"]
    tw, pw = stats.ttest_ind(wed, rest, equal_var=False)
    print(f"{sym}: {' | '.join(parts)}")
    print(f"     ANOVA p={pA:.3f}; Wed-vs-rest diff={wed.mean()-rest.mean():+.3f} p(two-sided)={pw:.3f}")

print("\n=== E. Holiday / half-day sensitivity ===")
for sym in INSTRUMENTS:
    z = series[sym]
    in_sample_special = sorted(set(z["date"]) & SPECIAL)
    v1 = z.loc[~z["date"].isin(SPECIAL), "z"]
    v2 = z.loc[~z["date"].isin(SPECIAL | ADJACENT), "z"]
    t0, p0 = one_sided_p(z["z"]); t1, p1 = one_sided_p(v1); t2_, p2_ = one_sided_p(v2)
    print(f"{sym}: special days present in sample after coverage filter: "
          f"{[str(d) for d in in_sample_special] or 'none'}")
    print(f"     baseline N={len(z)} mean={z['z'].mean():+.3f} p1s={p0:.2e} | "
          f"excl-special N={len(v1)} mean={v1.mean():+.3f} p1s={p1:.2e} | "
          f"excl-special+adjacent N={len(v2)} mean={v2.mean():+.3f} p1s={p2_:.2e}")
