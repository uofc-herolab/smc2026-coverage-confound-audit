# Paper Card — mathot2018_pupil_preprocessing

## Full citation (APA)
- Mathôt, S., Fabius, J., Van Heusden, E., & Van der Stigchel, S. (2018). Safe and sensible preprocessing and baseline correction of pupil-size data. *Behavior Research Methods, 50*(1), 94–106.

## Link / DOI
- https://doi.org/10.3758/s13428-017-1007-2

## Problem (1–3 sentences)
- J3 uses pupil diameter as a physiological workload proxy for CSAAB / CS-AAB.
- Pupil data is sensitive but can be confounded by blinks, tracking loss, and (especially) luminance.

## Approach (what they did)
- Provides “safe and sensible” recommendations for preprocessing and baseline correction to avoid spurious effects.

## Key recommendations (J3-relevant)
- Mark invalid data (blinks/tracking loss) before analysis.
- Use subtractive baseline correction (size − baseline).
- Visually inspect corrected vs uncorrected traces for artifacts.
- Respect physiological latency (~220 ms).
- Remove outlier trials with abnormal baseline values.

## Limitations / failure modes
- Luminance/light reflex is a major confound; requires strict lighting SOP.
- Pupil reflects arousal as well as workload.

## What we reuse (for J3)
- Preprocessing + baseline correction SOP for Pupil Core.
- Clear QC/exclusion criteria for pupil traces.
- Lighting control requirements.

## What we must NOT repeat (avoid redundancy vs C3/C1/C2)
- Don’t compute τ(t) from raw pupil without correction + QC.
