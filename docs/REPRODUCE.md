# Reproducing paper outputs (high level)

This repository does not distribute CASAS or TIHM data. After obtaining datasets and producing the feature tables described in the manuscript, set file paths in `configs/locked.yaml` and run the evaluation script(s).

Expected outputs (paper):
- Table II: out-of-fold ROC-AUC and AUPRC for Cov3 / CovPP / All with paired deltas and swap-null p-values
- Fig. 2: ROC-AUC bar plot across tasks
- Fig. 3: leakage audit summary (counts of CovPP descriptors with out-of-fold R^2 above thresholds)

Notes:
- TIHM CovPP uses fold-wise ridge residualization (alpha=1.0 fixed; no tuning) of the CovPP extra descriptors w.r.t. Cov3, then concatenates [Cov3, residuals].
