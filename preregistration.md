# Preregistration: Confirmatory Test of the 10:15–10:30 ET Intraday Volume Anomaly in CME Equity Index and Gold Futures

**Preregistration date:** 2026-07-23
**Specification frozen as of:** 2026-07-14 (no changes made after that date)
**Author:** [name / pseudonym]
**Status:** Registered before analysis of any confirmatory data. This document will not be edited after commit. Any deviation will be reported as a deviation.

---

## 1. Background (exploratory phase, completed)

Between 2026-07-08 and 2026-07-14 a recurring 1-minute volume surge was observed by eye in the 10:15–10:30 ET window across CME futures. An exploratory analysis was run on 2026-07-14:

- **Sample:** 49 trading days, 2026-05-04 to 2026-07-14, 5-minute bars (yfinance continuous contracts ES=F, MES=F, GC=F, MGC=F), plus 1-minute bars for the most recent 8 days.
- **Method:** RTH only (09:30–16:00 ET), 26 fifteen-minute buckets per day, per-day z-score of bucket volume, one-sample t-test on the 10:15 bucket.
- **Results:** mean z of the 10:15–10:30 bucket: ES +0.74, MES +1.20, GC +1.07, MGC +1.24; share of days with z>0: 92–98%; p-values 9.2×10⁻¹¹ to 6.3×10⁻¹⁵. Minute-level profile shows twin peaks at ~10:16 and ~10:33.
- **Falsified candidate mechanisms:** 10:00 ET scheduled data releases (strongest surge day had no releases); Wednesday EIA (Wednesday z below non-Wednesday).
- **Additional exploratory finding:** micro contracts show systematically higher z than full-size counterparts (MES−ES = +0.45; MGC−GC = +0.17; daily z correlation micro/full = 0.96 / 0.88), consistent with elevated retail order-flow concentration.

**Honesty note on selection:** the 10:15 bucket was selected *after* visual inspection of the full intraday profile. The exploratory p-values therefore carry a selection effect over 26 buckets. Bonferroni correction (×26) leaves all four results significant, but the exploratory sample cannot serve as confirmation of a hypothesis it generated. Hence this preregistered out-of-sample test.

## 2. Confirmatory hypotheses (frozen)

**H1 (primary):** In each of ES, MES, GC, MGC, the mean per-day z-score of RTH volume in the 10:15–10:30 ET bucket is greater than 0 over the confirmatory sample.

**H2 (secondary):** The mean per-day z-score difference (MES − ES) and (MGC − GC) for the 10:15–10:30 bucket is greater than 0 over the confirmatory sample.

No other hypotheses will be tested on the confirmatory sample.

## 3. Confirmatory sample (frozen)

- The first **30 qualifying trading days** beginning **2026-07-15** (expected completion ≈ 2026-08-25).
- **Qualifying day:** a regular CME trading day that is not a CME holiday or early-close (half) day, and for which the RTH 5-minute bar series for the given instrument has ≥ 95% of expected bars. Non-qualifying days are skipped and do not count toward the 30.
- Data source: yfinance continuous front contracts ES=F, MES=F, GC=F, MGC=F, 5-minute bars, timestamps converted to America/New_York. Raw pulls are archived locally at least weekly (yfinance 5-minute history is limited to ~60 days lookback), but **no bucket/z analysis is run on confirmatory data before the sample is complete**.

## 4. Analysis (frozen, identical to 2026-07-14 exploratory method)

1. Restrict to RTH 09:30–16:00 ET.
2. Partition each day into 26 fifteen-minute buckets; sum volume per bucket.
3. Per day: z = (bucket volume − mean of that day's 26 buckets) / SD of that day's 26 buckets.
4. Per instrument: one-sample t-test of the daily 10:15-bucket z-scores, one-sided (H0: mean ≤ 0; H1: mean > 0).
5. **Significance criterion (primary):** α = 0.05 with Bonferroni correction across the four instruments (per-test threshold p < 0.0125). H1 is *confirmed* only if all four instruments pass. Partial outcomes (0–3 of 4 passing) will be reported exactly as such, labeled "not confirmed."
6. **H2:** one-sample t-test on daily (MES−ES) and (MGC−GC) z differences, one-sided, α = 0.05, Bonferroni ×2 (p < 0.025), both must pass for confirmation.
7. The analysis is executed **once**, after the 30th qualifying day, using the frozen script `analysis_frozen.py` committed alongside this document. No parameter, bucket, window, or test may be altered.

## 5. Explicitly out of scope for this test

- Mechanism identification for the 10:16 / 10:33 twin peaks (requires tick-level / order-flow data; surviving hypothesis: scheduled programmatic execution). Reported as an open question.
- Gold–equity lead-lag analysis.
- Any price-direction or profitability claim. This study concerns volume seasonality only.

## 6. Known limitations (stated in advance)

- Sample covers a single regime window (mid-2026); cross-year stability is untestable with free data and is left to future work.
- Entire sample lies within EDT; no DST boundary is crossed.
- yfinance continuous-contract volume splicing around futures roll dates may distribute volume across front/next contracts; roll weeks are not excluded (matching the exploratory method) and this is acknowledged as noise, biasing against H1 rather than toward it.
- Exploratory and confirmatory samples are adjacent in time; persistence over 30 further days demonstrates short-horizon robustness, not permanence.

## 7. Integrity statement

As of the preregistration date, no bucket-level or z-score analysis has been performed on any data dated after 2026-07-14. Raw data pulled after that date has been archived without analysis. The author will report any violation of this statement as a protocol deviation.

## 8. Reporting commitment

The full result — confirmed, partially confirmed, or falsified — will be published together with the raw data, the frozen script, and this document, regardless of outcome.
