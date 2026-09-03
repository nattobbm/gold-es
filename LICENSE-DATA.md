# License for text, results and data

`LICENSE` (MIT) covers the **software** in this repository — all `*.py` files,
including everything under `tools/`.

**Everything else in this repository is licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).**

That is: `preregistration.md`, `results.md`, `robustness_exploratory.md`,
`README.md`, `results_stdout_2026-08-30.txt`, the `.csv` files at the
repository root, everything under `archive/` and `data/`, and the timestamp
manifests and `.ots` proofs.

Copyright (c) 2026 nattobbm.
Full legal code: https://creativecommons.org/licenses/by/4.0/legalcode

---

## What you may do

Share and adapt this material **for any purpose, including commercially** —
read it, run it, quote it, teach from it, extend it, build a product on it.

## The one condition

**Give appropriate credit**, link to the license, and indicate if you made
changes. This is the only condition, and it is not waivable.

## How to give credit

Use GitHub's "Cite this repository" button, or `CITATION.cff`, or:

> nattobbm (2026). *Intraday Volume Anomaly: the 10:15–10:30 ET Window in CME
> Futures — a preregistered study.* GitHub repository,
> https://github.com/nattobbm/gold-es. Preregistration commit `9a59771`
> (2026-07-23), hash-attested in Bitcoin block 960824 (2026-08-03).

If your point concerns the fact that the specification predates the data,
cite the preregistration commit and the block — those are the parts a reader
can verify without trusting anyone.

## What no license here grants

Authorship. Presenting this work, its specification, its results, or its data
as your own — or republishing it without attribution — falls outside both
licenses.

Unusually for a research repository, the priority claim does not rest on the
author's word or on GitHub's records. The SHA256 hashes of the frozen
specification and analysis script were committed to the Bitcoin blockchain on
2026-08-03, twenty-two days before the confirmatory sample closed. Any third
party can verify independently that this content existed on that date. See the
*Independent timestamping* section of `README.md`.

## Note on the underlying market data

The price and volume series were retrieved from Yahoo Finance via the
`yfinance` library and are redistributed here solely as the evidentiary record
of a preregistered study, so the published result can be independently
reproduced. The author claims no ownership of the underlying market data and
licenses only their own selection, arrangement and annotation of it. Anyone
intending large-scale or commercial redistribution of the raw series should
obtain it from the exchange or a licensed vendor.
