# Paper Card — scheme_englehart2011_emg_pr_review

## Full citation (APA)
- Scheme, E., & Englehart, K. (2011). Electromyogram pattern recognition for control of powered upper-limb prostheses: State of the art and challenges for clinical use. *Journal of Rehabilitation Research and Development, 48*(6), 643–660.

## Link / DOI
- https://doi.org/10.1682/JRRD.2010.09.0177

## Problem (1–3 sentences)
- Pattern recognition myoelectric control is promising but clinically challenged by non-stationarity (electrode shift, fatigue, limb position effects).
- These failures increase monitoring burden and reduce real-world usability.

## Approach (what they did)
- Review of PR EMG control pipeline, common features/classifiers, and barriers to clinical translation.

## PR pipeline (J3-relevant)
- Features: time-domain features (MAV, RMS, waveform length).
- Classifiers: LDA as practical real-time baseline.
- Training: supervised calibration protocols.

## Known limitations / failure modes
- Accuracy degrades under electrode shift, fatigue, and limb position changes.
- Lab results overestimate real-world performance.

## What we reuse (for J3)
- Baseline intent decoder architecture outputs p_u(g) over grasp classes.
- Motivation to treat PR output as probabilistic input to shared autonomy.

## What we must NOT repeat (avoid redundancy vs C3/C1/C2)
- Don’t assume classifier confidence is calibrated; calibrate probabilities before using c_u/entropy for ALI/τ(t).
