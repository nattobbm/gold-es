"""
FROZEN CONFIRMATORY ANALYSIS — do not edit after preregistration commit.
Spec frozen 2026-07-14; preregistered 2026-07-23.
Run ONCE, after the 30th qualifying trading day (expected ~2026-08-25).

Input : CSV files of 5-minute bars per instrument (columns: datetime, volume),
        timestamps in America/New_York or convertible; RTH filtering done here.
Output: per-instrument one-sided t-test on the 10:15-10:30 bucket z-scores (H1),
        and micro-minus-full z-difference tests (H2), printed verbatim.
"""

import sys
import pandas as pd
import numpy as np
from scipy import stats

INSTRUMENTS = ["ES", "MES", "GC", "MGC"]          # files: data/{sym}.csv
CONFIRM_START = "2026-07-15"
N_DAYS = 30                                        # first 30 qualifying days
RTH_START, RTH_END = "09:30", "16:00"
BUCKET_MIN = 15                                    # 26 buckets per RTH day
TARGET_BUCKET = "10:15"                            # bucket label = start time
MIN_BAR_COVERAGE = 0.95                            # qualifying-day threshold
ALPHA_H1 = 0.05 / 4                                # Bonferroni x4
ALPHA_H2 = 0.05 / 2                                # Bonferroni x2


def daily_bucket_z(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-day z-score of each 15-min RTH bucket."""
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    if df["datetime"].dt.tz is None:
        df["datetime"] = df["datetime"].dt.tz_localize("America/New_York")
    else:
        df["datetime"] = df["datetime"].dt.tz_convert("America/New_York")
    df = df.set_index("datetime").between_time(RTH_START, RTH_END, inclusive="left")
    df["date"] = df.index.date
    df["bucket"] = df.index.floor(f"{BUCKET_MIN}min").strftime("%H:%M")

    expected_bars = 78                             # 6.5h of 5-min bars
    rows = []
    for date, g in df.groupby("date"):
        if len(g) < MIN_BAR_COVERAGE * expected_bars:
            continue                               # non-qualifying day: skip
        b = g.groupby("bucket")["volume"].sum()
        if len(b) < 26 or b.std(ddof=1) == 0:
            continue
        z = (b - b.mean()) / b.std(ddof=1)
        rows.append({"date": date, "z": z.get(TARGET_BUCKET, np.nan)})
    out = pd.DataFrame(rows).dropna().sort_values("date")
    return out


def main() -> None:
    series = {}
    for sym in INSTRUMENTS:
        df = pd.read_csv(f"data/{sym}.csv")
        z = daily_bucket_z(df)
        z = z[z["date"] >= pd.to_datetime(CONFIRM_START).date()].head(N_DAYS)
        if len(z) < N_DAYS:
            print(f"[{sym}] only {len(z)} qualifying days — sample incomplete, ABORT.")
            sys.exit(1)
        series[sym] = z.set_index("date")["z"]

    print("=== H1: 10:15-10:30 bucket z > 0, one-sided, alpha=0.0125 each ===")
    h1_pass = []
    for sym in INSTRUMENTS:
        s = series[sym]
        t, p_two = stats.ttest_1samp(s, 0.0)
        p = p_two / 2 if t > 0 else 1 - p_two / 2
        ok = p < ALPHA_H1
        h1_pass.append(ok)
        print(f"{sym}: N={len(s)} mean_z={s.mean():+.3f} t={t:.2f} "
              f"p(one-sided)={p:.2e} -> {'PASS' if ok else 'FAIL'}")
    print(f"H1 overall: {'CONFIRMED' if all(h1_pass) else 'NOT CONFIRMED'} "
          f"({sum(h1_pass)}/4 passed)")

    print("\n=== H2: micro - full z difference > 0, one-sided, alpha=0.025 each ===")
    h2_pass = []
    for micro, full in (("MES", "ES"), ("MGC", "GC")):
        d = (series[micro] - series[full]).dropna()
        t, p_two = stats.ttest_1samp(d, 0.0)
        p = p_two / 2 if t > 0 else 1 - p_two / 2
        ok = p < ALPHA_H2
        h2_pass.append(ok)
        print(f"{micro}-{full}: N={len(d)} mean_diff={d.mean():+.3f} t={t:.2f} "
              f"p(one-sided)={p:.2e} -> {'PASS' if ok else 'FAIL'}")
    print(f"H2 overall: {'CONFIRMED' if all(h2_pass) else 'NOT CONFIRMED'} "
          f"({sum(h2_pass)}/2 passed)")


if __name__ == "__main__":
    main()
