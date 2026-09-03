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

**The preregistration (frozen 2026-07-23, never edited)**
- `preregistration.md` — frozen hypotheses, sample and exclusion rules, significance criteria, limitations, integrity statement.
- `analysis_frozen.py` — the confirmatory test as frozen. Not edited; byte-identical to its 2026-07-23 version, and its SHA256 is attested in Bitcoin block 960824.

**The result**
- `results.md` — full confirmatory report: verbatim script output, decisions against the preregistered criteria, exploratory-vs-confirmatory comparison, the marginal finding stated as marginal, protocol deviations, limitations, mechanism discussion.
- `results_stdout_2026-08-30.txt` — raw stdout of the single frozen run.
- `robustness_exploratory.md` — multiplicity correction (Bonferroni ×26 and ×104), split-half stability, weekday decomposition, holiday sensitivity, and the power analysis. All computed on exploratory data only, all committed before the confirmatory sample closed.

**Data**
- `*_1m.csv`, `*_5m.csv` (repo root) — raw exploratory-sample data, 2026-05-04 → 2026-07-14.
- `archive/pull_YYYY-MM-DD/` — dated raw pulls. Those dated on or before 2026-08-25 were made during the confirmatory period and were archived without being analyzed; later pulls are ordinary post-study collection.
- `data/{SYM}.csv` — the exact inputs fed to the frozen script on 2026-08-30 (staged from `archive/pull_2026-08-30/`; column `time` renamed to `datetime`, nothing else changed).

**Tooling** (`tools/`) — `weekly_archive.py` (scheduled data pulls), `sample_readiness_check.py` (bar-count-only completeness check), `stage_for_scoring.py` (file placement), `robustness_exploratory.py`, `power_analysis.py`, `confirmatory_descriptives.py`.

**Timestamp proofs** — `*.ots`, `MANIFEST_sha256_2026-08-03.txt`. See *Independent timestamping* below.

## Exploratory findings (superseded by the confirmatory test above)

Mean per-day z-score of the 10:15–10:30 bucket over 49 days, 2026-05-04 → 2026-07-14: ES +0.74, MES +1.20, GC +1.07, MGC +1.24; z > 0 on 92–98% of days. Two candidate mechanisms falsified (10:00 ET data releases; Wednesday EIA). Minute-level profile shows twin peaks near 10:16 and 10:33.

These figures were the *hypothesis-generating* sample and were never treated as proof. The confirmatory test has since been run: the effect persisted in all four contracts at a **smaller** magnitude (see the attenuation note above). The mechanism remains unresolved; the surviving hypothesis is scheduled programmatic execution, and separating it requires tick-level data.

## Why the commit history matters

The point of this repo is the timeline: the specification was publicly frozen **before** the confirmatory data existed, let alone was examined. That commitment is now discharged — the sample closed on 2026-08-25, the frozen script was run once on 2026-08-30, and the result was published as-is. The history has not been rewritten and will not be.

The order of events is checkable by anyone: preregistration commit `9a59771` (2026-07-23) → blockchain attestation of its hash (2026-08-03) → dated archive commits through the confirmatory window → `results.md` (2026-08-30).

## License and citation

**Use it freely. Just say where it came from.**

- Code (`*.py`, `tools/`) — MIT.
- Text, results and data (`preregistration.md`, `results.md`, `robustness_exploratory.md`, this README, the CSVs, `archive/`, `data/`) — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), see [`LICENSE-DATA.md`](LICENSE-DATA.md).

Read, run, quote, teach from, extend, or build a product on this — commercially or not — with one condition that is not waived: **credit the author and link back to this repository.** Use GitHub's "Cite this repository" button, or `CITATION.cff`, or:

> nattobbm (2026). *Intraday Volume Anomaly: the 10:15–10:30 ET Window in CME Futures — a preregistered study.* GitHub repository, https://github.com/nattobbm/gold-es. Preregistration commit `9a59771` (2026-07-23), hash-attested in Bitcoin block 960824 (2026-08-03).

The only thing no license here grants is authorship: presenting this work, its specification, its results, or its data as your own is outside all of the above — and, unusually for a research repository, the priority claim does not rest on anyone's word. It is verifiable against a public blockchain by any third party, as described next. Full terms: [`LICENSE`](LICENSE) (code) and [`LICENSE-DATA.md`](LICENSE-DATA.md) (everything else).

## Independent timestamping

Git commit dates are author-reported, so two independent attestations back the timeline:

1. **GH Archive** — the 2026-07-23/24 public push events to this repository are permanently recorded by the third-party [GH Archive](https://www.gharchive.org/) project, independent of this repo's history.
2. **OpenTimestamps** — on 2026-08-03 (before the confirmatory sample completed and before any confirmatory analysis), SHA256 hashes of the frozen files (`preregistration.md`, `analysis_frozen.py`, the exploratory CSVs via `MANIFEST_sha256_2026-08-03.txt`) were committed to the Bitcoin blockchain via [OpenTimestamps](https://opentimestamps.org/). The `.ots` proof files in this repo now carry their **completed Bitcoin attestations** (blocks 960824, 960827, 960856, 961002; block 960824 was mined 2026-08-03 05:05:26 UTC). Verify with `ots verify <file>.ots` against a Bitcoin node, or inspect with `ots info <file>.ots`.

   This means the content of the frozen specification and analysis script as of 2026-08-03 is provable independently of this repository, GitHub, and the authors.
