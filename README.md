# Intraday Volume Anomaly: the 10:15–10:30 ET Window in CME Futures

A preregistered, fully reproducible study of a recurring intraday volume surge in the 10:15–10:30 ET window, observed across four CME futures contracts: ES, MES (E-mini / Micro E-mini S&P 500) and GC, MGC (Gold / Micro Gold).

## Status: confirmatory waiting period

- **2026-07-14** — exploratory analysis completed (49 trading days, 2026-05-04 to 2026-07-14). The effect was found by visual inspection first, then tested; exploratory p-values therefore carry a selection effect over 26 intraday buckets, which is why they are not treated as confirmation.
- **2026-07-23** — specification, analysis script, and raw data committed here, frozen. See `preregistration.md` for the exact hypotheses, sample definition, and decision rules.
- **Now → ~2026-08-25** — confirmatory data (the first 30 qualifying trading days from 2026-07-15) accrues. Raw data is archived weekly **without being analyzed**.
- **~2026-08-25** — `analysis_frozen.py` is run once on the confirmatory sample. The result — confirmed, partial, or falsified — will be published here as-is.

## Repository contents

- `preregistration.md` — frozen hypotheses (H1: 10:15–10:30 bucket volume z-score > 0 in all four contracts; H2: micro contracts show higher z than full-size, consistent with retail order-flow concentration), sample and exclusion rules, significance criteria, limitations, integrity statement.
- `analysis_frozen.py` — the confirmatory test, frozen at preregistration. Not to be edited.
- `*_1m.csv`, `*_5m.csv` — raw exploratory-sample data (yfinance continuous contracts, 1-minute and 5-minute bars). Confirmatory-sample archives are added by later commits, marked "archived, not analyzed."

## Exploratory findings (to be re-tested, not taken as proven)

Mean per-day z-score of the 10:15–10:30 bucket over 49 days: ES +0.74, MES +1.20, GC +1.07, MGC +1.24; z > 0 on 92–98% of days. Two candidate mechanisms falsified (10:00 ET data releases; Wednesday EIA). Minute-level profile shows twin peaks near 10:16 and 10:33; the mechanism is unresolved (surviving hypothesis: scheduled programmatic execution) and is explicitly out of scope for the confirmatory test.

## Why the commit history matters

The point of this repo is the timeline: the specification is publicly frozen *before* the confirmatory data is examined. Commit timestamps are the notarization. The history will not be rewritten.

## Independent timestamping

Git commit dates are author-reported, so two independent attestations back the timeline:

1. **GH Archive** — the 2026-07-23/24 public push events to this repository are permanently recorded by the third-party [GH Archive](https://www.gharchive.org/) project, independent of this repo's history.
2. **OpenTimestamps** — on 2026-08-03 (before the confirmatory sample completes and before any confirmatory analysis), SHA256 hashes of the frozen files (`preregistration.md`, `analysis_frozen.py`, the exploratory CSVs via `MANIFEST_sha256_2026-08-03.txt`) were committed to the Bitcoin blockchain via [OpenTimestamps](https://opentimestamps.org/). The `.ots` proof files are in this repo; verify with `ots verify <file>.ots` (proofs will be upgraded to their final Bitcoin attestation once aggregated).
