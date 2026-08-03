# -*- coding: utf-8 -*-
"""Weekly confirmatory-period data archive (preregistration phase-1 routine).

Run by Windows Task Scheduler every Saturday 12:00 ET.
Pulls 5m (60d) + 1m (8d) bars for ES/MES/GC/MGC via yfinance,
stores them under archive/pull_YYYY-MM-DD/, logs row count + date
range ONLY (archived, not analyzed), commits with the fixed message
and pushes.

Idempotent: exits without action if today's archive dir already exists.
Log: ../archive_log.txt (outside the repo).
"""
import datetime
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(os.path.dirname(REPO), "archive_log.txt")
TODAY = datetime.date.today().isoformat()
OUTDIR = os.path.join(REPO, "archive", f"pull_{TODAY}")

JOBS = [
    ("ES",  "ES=F",  "5m", "60d"),
    ("MES", "MES=F", "5m", "60d"),
    ("GC",  "GC=F",  "5m", "60d"),
    ("MGC", "MGC=F", "5m", "60d"),
    ("ES",  "ES=F",  "1m", "8d"),
    ("MES", "MES=F", "1m", "8d"),
    ("GC",  "GC=F",  "1m", "8d"),
    ("MGC", "MGC=F", "1m", "8d"),
]


def log(msg):
    line = f"{datetime.datetime.now().isoformat(timespec='seconds')}  {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def git(*args):
    r = subprocess.run(["git", "-C", REPO, *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        log(f"GIT FAIL git {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r.returncode == 0


def main():
    if os.path.isdir(OUTDIR):
        log(f"pull_{TODAY} already exists - nothing to do")
        return 0

    git("pull", "--ff-only")

    import pandas as pd
    import yfinance as yf

    os.makedirs(OUTDIR, exist_ok=True)
    ok_5m = 0
    for name, sym, iv, per in JOBS:
        try:
            df = yf.download(sym, period=per, interval=iv,
                             progress=False, auto_adjust=False)
            if df.empty:
                log(f"[{name} {iv}] EMPTY - skipped")
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c[0] for c in df.columns]
            df = df.reset_index()
            tcol = "Datetime" if "Datetime" in df.columns else df.columns[0]
            out = df[[tcol, "Open", "High", "Low", "Close", "Volume"]].copy()
            out.columns = ["time", "open", "high", "low", "close", "volume"]
            out["time"] = (pd.to_datetime(out["time"], utc=True)
                           .dt.tz_convert("America/New_York"))
            out.to_csv(os.path.join(OUTDIR, f"{name}_{iv}.csv"), index=False)
            log(f"[{name} {iv}] rows={len(out)}  "
                f"{out['time'].min()} -> {out['time'].max()}")
            if iv == "5m":
                ok_5m += 1
        except Exception as e:
            log(f"[{name} {iv}] FAILED: {e}")

    if not os.listdir(OUTDIR):
        os.rmdir(OUTDIR)
        log(f"pull_{TODAY} INCOMPLETE: nothing pulled, no commit. "
            f"RERUN MANUALLY.")
        return 1

    if ok_5m < 4:
        log(f"pull_{TODAY} WARNING: only {ok_5m}/4 5m files pulled - "
            f"committing partial archive, RERUN MANUALLY for the rest.")

    msg = (f"Data archive {TODAY} "
           f"(confirmatory period; archived, not analyzed)")
    if not (git("add", os.path.join("archive", f"pull_{TODAY}"))
            and git("commit", "-m", msg)
            and git("push", "origin", "main")):
        log(f"pull_{TODAY} data saved locally but COMMIT/PUSH FAILED - "
            f"push manually.")
        return 1

    log(f"pull_{TODAY} archived, committed and pushed "
        f"({ok_5m}/4 5m files complete)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
