# Measures + Scoring Spec v1 (Week 2)

## Objective
Lock the **final measurement battery** and a **reproducible scoring pipeline** before any data collection.

This corresponds to Week 2 in the plan: lock measures + scoring scripts + measurement ledger【Week 2 plan】.

## Primary outcomes (recommended)
1) Agency:
- SoAS (report SoPA and SoNA separately)
- Plus a simple per-block agency rating (0–100 slider): `agency_block_rating`

2) Workload:
- NASA-TLX (Raw TLX = mean of 6 subscales)

3) Performance (from task logs, not surveys):
- success/fail, time, error counts (defined later in Week 3 logging schema)

## Secondary outcomes (recommended)
- Trust in automation scale (select and lock the exact scale this week)
- Ownership/embodiment short form (select and lock this week)
- Optional: PROS-TLX if the task strongly mimics prosthesis use

## Survey structure (forms)
- **One form per block**: TLX + block agency rating (+ trust/embodiment if you keep them per block)
- **Final post-study form**: longer trust + embodiment + open-ended comments

## CSV column naming (to make scoring easy)
Design your form or rename columns after export so the CSV has:

### IDs
- subject_id
- session_id
- block_id
- condition

### Agency
- sopa_01, sopa_02, ... (SoPA items)
- sona_01, sona_02, ... (SoNA items)
- agency_block_rating  (0–100)

### NASA-TLX
- tlx_mental
- tlx_physical
- tlx_temporal
- tlx_performance
- tlx_effort
- tlx_frustration

### Trust (placeholder)
- trust_01, trust_02, ...

### Embodiment (placeholder)
- embod_01, embod_02, ...

## Scoring rules
- SoPA = mean of all `sopa_*` columns (ignore blanks)
- SoNA = mean of all `sona_*` columns (ignore blanks)
- TLX_RTLX = mean of the 6 tlx_* subscales (ignore blanks)
- Trust = mean of trust_* (ignore blanks)
- Embodiment = mean of embod_* (ignore blanks)

## Physiology metrics to compute later (Week 2 definition)
From Delsys:
- EMG effort: RMS/MAV normalized to a calibration contraction
- Cocontraction index: overlap between antagonist pairs (define which muscles later)
- IMU smoothness proxy: jerk or spectral arc length proxy (specify later)

## Outputs
- `code/score_surveys.py` produces: `surveys/scores.csv`
- `measures/measurement_ledger_v1.csv` (tracked) and optional .xlsx

