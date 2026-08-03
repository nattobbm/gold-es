# -*- coding: utf-8 -*-
"""Statistical power of the frozen confirmatory test (n=30), computed ONLY from
exploratory effect sizes (data <= 2026-07-14). Registered-reports convention:
a prereg should state expected power; ours didn't, so we add it post hoc to the
robustness doc, clearly labeled as computed after preregistration.
"""
import os
import numpy as np
import pandas as pd
from scipy import stats

REPO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gold-es")
INSTRUMENTS = ["ES", "MES", "GC", "MGC"]
EXPLORATORY_END = pd.Timestamp("2026-07-14").date()
N_CONF = 30
ALPHA_H1 = 0.0125
ALPHA_H2 = 0.025


def daily_bucket_z(df):
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["time"], utc=True).dt.tz_convert("America/New_York")
    df = df.set_index("datetime").between_time("09:30", "16:00", inclusive="left")
    df["date"] = df.index.date
    df["bucket"] = df.index.floor("15min").strftime("%H:%M")
    rows = []
    for date, g in df.groupby("date"):
        if date > EXPLORATORY_END or len(g) < 0.95 * 78:
            continue
        b = g.groupby("bucket")["volume"].sum()
        if len(b) < 26 or b.std(ddof=1) == 0:
            continue
        z = (b - b.mean()) / b.std(ddof=1)
        rows.append({"date": date, "z": z.get("10:15", np.nan)})
    return pd.DataFrame(rows).dropna().sort_values("date").set_index("date")["z"]


def power_one_sided(d, n, alpha):
    crit = stats.t.ppf(1 - alpha, df=n - 1)
    return 1 - stats.nct.cdf(crit, df=n - 1, nc=d * np.sqrt(n))


series = {s: daily_bucket_z(pd.read_csv(os.path.join(REPO, f"{s}_5m.csv")))
          for s in INSTRUMENTS}

print("=== H1 power at n=30, one-sided alpha=0.0125 (exploratory effect size) ===")
for sym in INSTRUMENTS:
    s = series[sym]
    d = s.mean() / s.std(ddof=1)
    print(f"{sym}: d={d:.3f}  power={power_one_sided(d, N_CONF, ALPHA_H1):.6f}")

print("\n=== H2 power at n=30, one-sided alpha=0.025 (exploratory effect size) ===")
for micro, full in (("MES", "ES"), ("MGC", "GC")):
    diff = (series[micro] - series[full]).dropna()
    d = diff.mean() / diff.std(ddof=1)
    print(f"{micro}-{full}: d={d:.3f}  power={power_one_sided(d, N_CONF, ALPHA_H2):.6f}")

print("\n=== Minimum detectable effect (power=0.80) ===")
for alpha, label in ((ALPHA_H1, "H1"), (ALPHA_H2, "H2")):
    lo, hi = 0.01, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if power_one_sided(mid, N_CONF, alpha) < 0.80:
            lo = mid
        else:
            hi = mid
    print(f"{label}: d_min(80% power, n=30, alpha={alpha}) = {hi:.3f}")
