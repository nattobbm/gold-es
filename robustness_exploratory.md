# Robustness Checks — Exploratory Sample Only

**Date of analysis:** 2026-08-02
**Data:** exploratory sample only, 49 qualifying trading days, 2026-05-04 → 2026-07-14 (the `{SYM}_5m.csv` files committed 2026-07-23). **No data after 2026-07-14 was analyzed.** The confirmatory sample remains untouched per the preregistration integrity statement.
**Method:** identical to the frozen specification (`analysis_frozen.py`): RTH 09:30–16:00 ET, 26 fifteen-minute buckets/day, per-day z-score of bucket volume, target bucket 10:15–10:30, qualifying day = ≥95% of 78 expected 5-minute bars. The frozen script itself was not modified; its bucket/z logic was replicated in a separate script.

These checks address the honesty note in preregistration §1: the 10:15 bucket was selected post hoc among 26 buckets, so exploratory significance must survive multiplicity correction and stability checks to justify the preregistered confirmation test. They will form the robustness section of the final report.

---

## 0. Baseline reproduction

| | N | mean z (↑ = surge) | t | p (one-sided) | days z>0 |
|---|---|---|---|---|---|
| ES | 49 | +0.743 | 8.25 | 4.6×10⁻¹¹ | 91.8% |
| MES | 49 | +1.197 | 11.15 | 3.2×10⁻¹⁵ | 95.9% |
| GC | 49 | +1.071 | 7.81 | 2.1×10⁻¹⁰ | 95.9% |
| MGC | 49 | +1.245 | 9.70 | 3.4×10⁻¹³ | 98.0% |

Mean z-scores reproduce preregistration §1 exactly (+0.74 / +1.20 / +1.07 / +1.24).

**Reporting-convention note (deviation-level: cosmetic):** the p-values quoted in preregistration §1 (9.2×10⁻¹¹ … 6.3×10⁻¹⁵) are **two-sided**; the values above are one-sided (exactly half). The frozen confirmatory test is one-sided as specified in §4; nothing in the frozen protocol changes. Noted here for consistency of the final report.

## 1. Bonferroni ×26 (post-hoc bucket selection)

Correcting each instrument's one-sided p for the 26 buckets the target was chosen from — and additionally ×4 for the four instruments (×104 total):

| | p ×26 | p ×104 | significant at α=0.05? |
|---|---|---|---|
| ES | 1.2×10⁻⁹ | 4.8×10⁻⁹ | yes (both) |
| MES | 8.2×10⁻¹⁴ | 3.3×10⁻¹³ | yes (both) |
| GC | 5.6×10⁻⁹ | 2.2×10⁻⁸ | yes (both) |
| MGC | 8.7×10⁻¹² | 3.5×10⁻¹¹ | yes (both) |

All four instruments survive the full ×104 correction. Selection effect alone cannot account for the exploratory result.

## 2. Split-half stability (chronological)

First 24 days vs last 25 days:

| | 1st half mean z | 1st half p (1s) | 2nd half mean z | 2nd half p (1s) | halves differ? (2-sided p) |
|---|---|---|---|---|---|
| ES | +0.684 | 1.2×10⁻⁵ | +0.801 | 7.6×10⁻⁷ | 0.52 |
| MES | +1.145 | 3.8×10⁻⁸ | +1.247 | 1.9×10⁻⁸ | 0.64 |
| GC | +1.030 | 1.6×10⁻⁵ | +1.111 | 2.9×10⁻⁶ | 0.77 |
| MGC | +1.194 | 3.2×10⁻⁷ | +1.293 | 2.3×10⁻⁷ | 0.70 |

Both halves are independently significant for every instrument; no half-to-half drift is detectable (all between-half p > 0.5, second half nominally slightly higher). The effect is not driven by a sub-period.

## 3. Weekday effect

Mean 10:15-bucket z by weekday (n per weekday 8–11):

| | Mon | Tue | Wed | Thu | Fri | ANOVA p | Wed − rest (2-sided p) |
|---|---|---|---|---|---|---|---|
| ES | +0.71 | +0.94 | +0.62 | +0.86 | +0.53 | 0.63 | −0.16 (0.53) |
| MES | +1.16 | +1.42 | +1.02 | +1.31 | +1.03 | 0.72 | −0.23 (0.42) |
| GC | +1.18 | +1.46 | +0.76 | +0.94 | +0.95 | 0.52 | −0.40 (0.27) |
| MGC | +1.41 | +1.55 | +0.99 | +1.04 | +1.19 | 0.59 | −0.32 (0.29) |

No weekday concentration (all ANOVA p > 0.5); the surge is present on every weekday. Wednesday is nominally the *lowest* weekday in all four instruments, consistent with the earlier falsification of the Wednesday-EIA mechanism (a 10:30 EIA-driven effect would make Wednesday highest).

## 4. Holiday / half-day sensitivity

CME special days inside the sample window: 2026-05-25 (Memorial Day), 2026-06-19 (Juneteenth), 2026-07-03 (Independence Day observed) — all early-close/closed days.

- The frozen ≥95%-coverage filter already removes all three from the sample: **0 special days present in the 49-day baseline**, so "excluding holidays/half-days" changes nothing by construction.
- Stricter variant — additionally excluding the 6 adjacent regular trading days (day before/after each special day), N 49→43:

| | baseline mean z | excl. adjacent mean z | excl. adjacent p (1s) |
|---|---|---|---|
| ES | +0.743 | +0.750 | 2.0×10⁻⁹ |
| MES | +1.197 | +1.210 | 5.0×10⁻¹³ |
| GC | +1.071 | +1.046 | 1.6×10⁻⁸ |
| MGC | +1.245 | +1.254 | 2.2×10⁻¹¹ |

Means move by ≤0.03; all results remain significant. Holiday-adjacent liquidity conditions do not drive the effect.

## 5. Statistical power of the frozen confirmatory test (added 2026-08-03, before scoring)

*The preregistration did not state a power analysis (a gap relative to registered-reports convention). It is added here — computed only from exploratory effect sizes (data ≤ 2026-07-14), before any confirmatory data is unblinded, and it changes nothing in the frozen protocol.*

Power of the frozen tests at n=30, assuming the exploratory effect sizes (Cohen's d = mean/SD of the daily z-series):

| test | d (exploratory) | power at n=30 |
|---|---|---|
| H1 ES | 1.18 | >0.999 |
| H1 MES | 1.59 | ≈1.000 |
| H1 GC | 1.12 | >0.999 |
| H1 MGC | 1.39 | ≈1.000 |
| H2 MES−ES | 1.90 | ≈1.000 |
| **H2 MGC−GC** | **0.37** | **0.51** |

Minimum detectable effect at 80% power, n=30: d ≈ 0.59 (H1), d ≈ 0.53 (H2).

**Interpretation committed in advance:** H1 and the equity leg of H2 are effectively guaranteed to pass *if* the exploratory effect sizes persist. The gold leg of H2 (MGC−GC, exploratory mean diff +0.17) is underpowered by design: even if the true effect equals the exploratory estimate, the frozen test fails ≈49% of the time. Therefore a "H2 not confirmed" outcome driven by the gold pair is consistent both with a smaller/absent effect and with insufficient power, and will be reported with this ambiguity stated — not reinterpreted after the fact. The frozen pass/fail criteria are unchanged.

---

## Conclusion

The exploratory effect survives (1) full multiplicity correction for post-hoc bucket and instrument selection, (2) chronological split-half replication, (3) weekday decomposition, and (4) holiday-adjacency exclusion. None of this substitutes for the preregistered out-of-sample confirmation (frozen sample: first 30 qualifying days from 2026-07-15; scoring ≈ 2026-08-25), but it rules out the most common ways a post-hoc-selected anomaly can be a statistical artifact of the exploratory sample itself.

*Limitations carried over unchanged from preregistration §6: single regime window, no DST boundary, continuous-contract roll splicing noise, adjacency of exploratory and confirmatory windows.*
