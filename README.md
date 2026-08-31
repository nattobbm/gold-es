# Intraday Volume Anomaly: the 10:15–10:30 ET Window in CME Futures

A preregistered, fully reproducible study of a recurring intraday volume surge in the 10:15–10:30 ET window, observed across four CME futures contracts: ES, MES (E-mini / Micro E-mini S&P 500) and GC, MGC (Gold / Micro Gold).

## Status: complete — both hypotheses confirmed out of sample

**See [`results.md`](results.md) for the full result, including the deviations and the weakest finding.**

- **2026-07-14** — exploratory analysis completed (49 trading days, 2026-05-04 to 2026-07-14). The effect was found by visual inspection first, then tested; exploratory p-values therefore carry a selection effect over 26 intraday buckets, which is why they were not treated as confirmation.
- **2026-07-23** — specification, analysis script, and raw data committed here, frozen. See `preregistration.md` for the exact hypotheses, sample definition, and decision rules.
- **2026-08-03** — SHA256 of the frozen files committed to the Bitcoin blockchain (see below). Robustness checks and a power analysis added, both using exploratory data only.
- **2026-07-15 → 2026-08-25** — confirmatory sample accrued (30 qualifying trading days). Raw data archived without being analyzed.
- **2026-08-30** — `analysis_frozen.py` run once, unmodified, after verifying it is byte-identical to the preregistered version and matches its blockchain-attested hash.

### Result

| hypothesis | outcome |
|---|---|
| **H1** — 10:15–10:30 ET bucket volume z > 0 in ES, MES, GC, MGC (Bonferroni ×4, all four must pass) | **CONFIRMED, 4/4** (mean z +0.64 / +1.12 / +0.76 / +0.97; p from 1.4×10⁻⁵ to 6.0×10⁻¹³) |
| **H2** — micro-minus-full z difference > 0 for MES−ES and MGC−GC (Bonferroni ×2, both must pass) | **CONFIRMED, 2/2** (+0.485, p = 6.3×10⁻¹⁰; +0.211, p = 0.0121) |

Two caveats stated up front, not buried: all four H1 effects **attenuated** out of sample (−6% for MES to −29% for GC), consistent with the declared selection effect in the exploratory phase. And **MGC−GC is marginal** — it clears its threshold by a factor of ~2 where the others clear theirs by 7–11 orders of magnitude, and a pre-committed power analysis put that specific test at only 51% power. It should be read as suggestive and re-tested, not as established. Mechanism remains unresolved.

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
2. **OpenTimestamps** — on 2026-08-03 (before the confirmatory sample completed and before any confirmatory analysis), SHA256 hashes of the frozen files (`preregistration.md`, `analysis_frozen.py`, the exploratory CSVs via `MANIFEST_sha256_2026-08-03.txt`) were committed to the Bitcoin blockchain via [OpenTimestamps](https://opentimestamps.org/). The `.ots` proof files in this repo now carry their **completed Bitcoin attestations** (blocks 960824, 960827, 960856, 961002; block 960824 was mined 2026-08-03 05:05:26 UTC). Verify with `ots verify <file>.ots` against a Bitcoin node, or inspect with `ots info <file>.ots`.

   This means the content of the frozen specification and analysis script as of 2026-08-03 is provable independently of this repository, GitHub, and the authors.
