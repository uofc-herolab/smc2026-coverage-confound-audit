# SMC 2026 Coverage Confound Audit (Cov3 / CovPP / All)

This repository supports reproducibility for:
"Confound-Aware Evaluation of Smart-Home Digital Biomarkers: Auditing Observation Intensity Dominance in Cognitive Status and Agitation"
(IEEE SMC 2026 submission).

## What this repo provides
- Locked evaluation protocol comparing Cov3, CovPP, and All
- Participant-disjoint (GroupKFold) out-of-fold evaluation
- Cluster bootstrap confidence intervals and cluster-aware swap-null permutation tests
- TIHM fold-wise ridge residualization (CovPP) with respect to Cov3

## What this repo does NOT provide
- This repository does not redistribute CASAS or TIHM data. Users must obtain datasets from their original sources.

## Quickstart
1) Create environment (see environment.yml)
2) Edit dataset paths (see configs/locked.yaml)
3) Run:
   python scripts/run_locked_eval.py --config configs/locked.yaml
