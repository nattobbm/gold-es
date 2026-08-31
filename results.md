# Confirmatory Results — the 10:15–10:30 ET Intraday Volume Anomaly

**Analysis run:** 2026-08-30
**Confirmatory sample:** 30 qualifying trading days, 2026-07-15 → 2026-08-25 (identical dates for all four instruments; the 30th qualifying day fell on 2026-08-25, matching the date projected in the preregistration)
**Script:** `analysis_frozen.py`, run once, unmodified
**Outcome: H1 CONFIRMED (4/4). H2 CONFIRMED (2/2).**

---

## 1. Pre-run integrity verification

Before execution, the frozen files were verified three ways:

| check | result |
|---|---|
| `git status` on `analysis_frozen.py`, `preregistration.md` | clean, no uncommitted modification |
| `git diff` against preregistration commit `9a59771` (2026-07-23) | empty — byte-identical to the preregistered version |
| SHA256 vs `MANIFEST_sha256_2026-08-03.txt`, whose hash is committed to **Bitcoin block 960824** (mined 2026-08-03 05:05:26 UTC) | exact match: `0e384e01…` (`analysis_frozen.py`), `bff1f3db…` (`preregistration.md`) |

The script that produced the results below is therefore provably the script that was frozen 22 days before the sample completed, independently of this repository, of GitHub, and of the author.

## 2. Raw output (verbatim)

```
=== H1: 10:15-10:30 bucket z > 0, one-sided, alpha=0.0125 each ===
ES: N=30 mean_z=+0.636 t=8.98 p(one-sided)=3.56e-10 -> PASS
MES: N=30 mean_z=+1.121 t=11.86 p(one-sided)=6.01e-13 -> PASS
GC: N=30 mean_z=+0.756 t=4.96 p(one-sided)=1.44e-05 -> PASS
MGC: N=30 mean_z=+0.967 t=7.37 p(one-sided)=2.00e-08 -> PASS
H1 overall: CONFIRMED (4/4 passed)

=== H2: micro - full z difference > 0, one-sided, alpha=0.025 each ===
MES-ES: N=30 mean_diff=+0.485 t=8.75 p(one-sided)=6.28e-10 -> PASS
MGC-GC: N=30 mean_diff=+0.211 t=2.38 p(one-sided)=1.21e-02 -> PASS
H2 overall: CONFIRMED (2/2 passed)
```

Full stdout is preserved in `results_stdout_2026-08-30.txt`.

## 3. Decisions against the preregistered criteria

**H1** — mean per-day z of the 10:15–10:30 ET bucket > 0, one-sided, Bonferroni ×4 (per-test p < 0.0125), all four must pass:

| instrument | N | mean z | t | p (one-sided) | p (two-sided)¹ | decision |
|---|---|---|---|---|---|---|
| ES | 30 | +0.636 | 8.98 | 3.56×10⁻¹⁰ | 7.12×10⁻¹⁰ | **PASS** |
| MES | 30 | +1.121 | 11.86 | 6.01×10⁻¹³ | 1.20×10⁻¹² | **PASS** |
| GC | 30 | +0.756 | 4.96 | 1.44×10⁻⁵ | 2.88×10⁻⁵ | **PASS** |
| MGC | 30 | +0.967 | 7.37 | 2.00×10⁻⁸ | 4.00×10⁻⁸ | **PASS** |

**H1: CONFIRMED (4/4).**

**H2** — mean per-day z difference (micro − full) > 0, one-sided, Bonferroni ×2 (per-test p < 0.025), both must pass:

| pair | N | mean diff | t | p (one-sided) | p (two-sided)¹ | decision |
|---|---|---|---|---|---|---|
| MES − ES | 30 | +0.485 | 8.75 | 6.28×10⁻¹⁰ | 1.26×10⁻⁹ | **PASS** |
| MGC − GC | 30 | +0.211 | 2.38 | 1.21×10⁻² | 2.42×10⁻² | **PASS** |

**H2: CONFIRMED (2/2).**

¹ Two-sided p values are a **reporting supplement, not the decision rule**. The decision rule is the one-sided test frozen in preregistration §4. The supplement was committed on 2026-08-03 — before the sample completed and before unblinding — because the exploratory p-values quoted in preregistration §1 were two-sided while the frozen test is one-sided, and both conventions should be visible. Every result above clears its Bonferroni threshold under **either** convention.

## 4. Descriptive context (not preregistered tests)

| instrument | median z | days with z > 0 | exploratory comparison |
|---|---|---|---|
| ES | +0.574 | 29/30 (96.7%) | exploratory 91.8% |
| MES | +0.998 | 30/30 (100%) | exploratory 95.9% |
| GC | +0.495 | 26/30 (86.7%) | exploratory 95.9% |
| MGC | +0.823 | 30/30 (100%) | exploratory 98.0% |

## 5. Exploratory vs confirmatory

| | exploratory (49 days, 05-04→07-14) | confirmatory (30 days, 07-15→08-25) | change |
|---|---|---|---|
| ES mean z | +0.743 | +0.636 | −0.107 (−14%) |
| MES mean z | +1.197 | +1.121 | −0.076 (−6%) |
| GC mean z | +1.071 | +0.756 | −0.315 (−29%) |
| MGC mean z | +1.245 | +0.967 | −0.278 (−22%) |
| MES − ES | +0.450 | +0.485 | +0.035 |
| MGC − GC | +0.170 | +0.211 | +0.041 |

**Reading this honestly:** every H1 effect **attenuated** out of sample — mildly for the equity contracts (−6% to −14%), substantially for gold (−22% to −29%). This is the expected signature of the selection effect declared in preregistration §1: the bucket was chosen after inspecting the exploratory profile, so the exploratory magnitudes were upward-biased and some regression toward the mean was predictable. What the confirmatory test establishes is that the effect **survives** out of sample at high significance, not that it is as large as the exploratory sample suggested. The micro-minus-full differences (H2) did not attenuate; both rose slightly.

## 6. The weakest result, stated plainly

**MGC − GC is the marginal result in this set** and should not be read with the same confidence as the other five:

- p = 0.0121 against a threshold of 0.025 — it clears Bonferroni, but by roughly a factor of 2, whereas the other five clear theirs by 7 to 11 orders of magnitude.
- A power analysis committed on 2026-08-03 (before unblinding, in `robustness_exploratory.md` §5) computed this leg's power at n=30 as **0.51** on the exploratory effect size. The pre-committed rule stated that a *failure* here would be reported as ambiguous between "small/absent effect" and "insufficient power". It did not fail — but a 51%-powered test passing is a favorable draw, not strong evidence. **The gold micro/full difference should be treated as suggestive and re-tested on a larger sample**, not as established at the strength of the other results.

The equity leg (MES − ES, p = 6.3×10⁻¹⁰) carries the confirmation of H2.

## 7. Protocol deviations

Reported per preregistration §7, including one procedural violation that had no effect on the test:

1. **Weekly archiving interrupted once.** Preregistration §3 committed to archiving raw pulls "at least weekly". The pull scheduled for 2026-08-22 did not run (the machine was powered off for that week; the automated task caught up on 2026-08-29). Effect on this test: **none.** yfinance's 5-minute history has a ~60-day lookback, so the 2026-08-30 archive (`archive/pull_2026-08-30/`, covering 2026-06-21 → 2026-08-30) re-covers the entire confirmatory window; no 5-minute bar used in this analysis was lost. The permanent loss is 1-minute data for 2026-08-15 → 2026-08-19 (1-minute history has an ~8-day lookback). 1-minute data is not used by the frozen test; it supports only the minute-level twin-peak profile, which preregistration §5 places out of scope for confirmation. This gap does constrain future mechanism work on that specific week.
2. **Reporting-convention inconsistency (cosmetic).** The exploratory p-values in preregistration §1 are two-sided; the frozen test is one-sided. No hypothesis, threshold, or procedure changed. Documented 2026-08-03; both conventions are reported in §3 above.
3. **File placement.** The frozen script reads `data/{SYM}.csv` with a `datetime` column; the archives are named `{SYM}_5m.csv` with a `time` column. Staging (`tools/stage_for_scoring.py`) copies and renames the column only — no row was filtered, reordered, or altered. The script performs its own RTH filtering, qualifying-day filtering, and 30-day truncation, so no discretion was exercised in sample selection.
4. **Additions made after preregistration but before unblinding:** the robustness checks (2026-08-02), the power analysis (2026-08-03), and the OpenTimestamps attestations (2026-08-03). None modified the frozen protocol.

No other deviation occurred. No analysis of confirmatory data was performed before this run; the only pre-run inspection was a bar-count check (`tools/sample_readiness_check.py`, which reads the timestamp column only) to determine whether the 30-day sample was complete.

## 8. Limitations

Carried from preregistration §6, unchanged:

- **Single regime window.** The whole study covers 2026-05-04 → 2026-08-25. Cross-year stability is untested and untestable with free data.
- **No DST boundary.** The entire sample lies within EDT.
- **Continuous-contract roll splicing.** yfinance continuous contracts may distribute volume across front/next contracts around roll dates; roll weeks were not excluded, matching the exploratory method. This adds noise and biases against H1 rather than toward it.
- **Adjacency.** Exploratory and confirmatory windows are contiguous. Persistence over 30 further days demonstrates short-horizon robustness, not permanence.
- **Mechanism unresolved.** See §9.
- **Added here:** the 1-minute data gap of 2026-08-15 → 2026-08-19 (see §7.1), and the reduced 1-minute coverage it implies for any future minute-level work on that week.

## 9. Mechanism: still open

The confirmatory test establishes *that* the 10:15–10:30 ET volume surge is real and persistent across four contracts, and that it is systematically stronger in micro contracts. It says nothing about *why*.

Falsified during the exploratory phase and not revisited here: 10:00 ET scheduled data releases; Wednesday EIA inventories.

The surviving hypothesis remains scheduled programmatic execution. Published work on intraday periodicity in algorithmic trading documents systematic clustering of trades shortly after round time marks, at 5- and 10-minute intervals, attributed to behavioral round-number preference in algorithm design rather than to cost advantages. The minute-level profile observed here (peaks near 10:16 and 10:33, i.e. just after the 10:15 and 10:30 marks) is consistent with that pattern, but consistency is not identification. Separating the order-flow composition of those peaks requires tick-level data (e.g. Databento CME direct feed) and remains out of scope.

The micro-minus-full result (H2) is consistent with elevated retail order-flow concentration in this window, but the design cannot distinguish retail participation from any other mechanism that would differentially affect micro contracts.

## 10. Reporting commitment, discharged

Preregistration §8 committed to publishing the full result — confirmed, partial, or falsified — together with the raw data, the frozen script, and the preregistration. The outcome was confirmatory; it is published here with the attenuation, the marginal gold leg, and the archiving lapse stated as prominently as the passes.
