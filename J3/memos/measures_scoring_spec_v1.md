# Measures + Scoring Spec v1 (Week 2 — Locked)

## Objective
Lock a scientifically defensible **measurement battery** and a reproducible **scoring pipeline** before any data collection.

This file intentionally avoids copying full questionnaire item wording into the repo.
Use your survey platform (Qualtrics / Google Forms) to host item text; in the repo we keep:
- citations
- column naming rules
- scoring rules
- code

---

## Locked instruments (Week 2 decision)

### Agency (Primary)
**Sense of Agency Scale (SoAS)** — Tapal et al. (2017)
- Output: **SoPA** and **SoNA** scored separately
- CSV columns:
  - `sopa_01 ... sopa_N`
  - `sona_01 ... sona_M`
- Scoring:
  - `SoPA = mean(sopa_*)`
  - `SoNA = mean(sona_*)`

> Note: We intentionally do not hardcode item counts; your form determines N/M. The scorer averages whatever `sopa_*` and `sona_*` are present.

### Workload (Primary)
**NASA‑TLX (Raw TLX / RTLX)** — Hart (2006)
- CSV columns (0–100 typical):
  - `tlx_mental`
  - `tlx_physical`
  - `tlx_temporal`
  - `tlx_performance`
  - `tlx_effort`
  - `tlx_frustration`
- Scoring:
  - `TLX_RTLX = mean(all 6 tlx_* subscales)`

### Trust (Secondary)
**Trust in Automation / “TIAS” style scale** — Jian, Bisantz, & Drury (2000)
- Rationale: short, widely used, sensitive to state changes; includes explicit distrust.
- Admin: recommended **once per controller condition** (UserOnly / ConfBlend / SetACSA / CS‑AAB).
- CSV columns (recommended naming):
  - Trust items: `tias_trust_01 ... tias_trust_07`
  - Distrust items: `tias_distrust_01 ... tias_distrust_05`
- Scoring outputs:
  - `TIAS_trust_mean = mean(tias_trust_*)`
  - `TIAS_distrust_mean = mean(tias_distrust_*)`
  - `TIAS_total_trust = mean( tias_trust_* plus reverse(tias_distrust_*) )`
- Reverse coding rule (for 1–7):
  - `reverse(x) = 8 - x`

> IMPORTANT: Don’t paste the full item text into the repo. Keep item wording in your survey tool and cite the paper.

### Embodiment / Ownership (Secondary)
**Prosthesis Embodiment Scale (PEmbS)** — Bekrater‑Bodmann (2020)
- Rationale: short (10 items), prosthesis‑focused, open access in the cited summary.
- Admin: recommended **end‑of‑session** for able‑bodied, optional per‑condition for amputees if time permits.
- CSV columns:
  - `pembs_01 ... pembs_10`
- Scoring:
  - `PEmbS_total = mean(pembs_01..pembs_10)`

> Subscales exist in the literature, but we do NOT implement subscales until we verify the exact item→factor mapping from the paper tables.

---

## Survey structure (practical default)
Define a “condition block” as the unit where the controller policy is fixed.

### Condition survey (after each condition block)
- NASA‑TLX (6 subscales)
- SoAS (SoPA + SoNA items)
- TIAS (trust + distrust items)
- Optional quick slider: `agency_block_rating` (0–100)

### Post‑study survey (end of session)
- PEmbS (10 items)
- 2 open-ended questions (optional but recommended):
  - “When did it feel most like YOU were controlling it?”
  - “When did it feel most like the SYSTEM took over?”

---

## Required IDs (in every survey export)
- `subject_id`
- `session_id`
- `block_id`
- `condition`

---

## Naming caution
In this project, **ALI = Agency Loss Index** (controller‑side metric).
Do NOT reuse “ALI” to mean “assistance-to-liberty” or any other ratio — pick a different acronym if you introduce that concept.

---

## Outputs produced by the scorer
`code/score_surveys.py` writes a scored CSV with:
- SoPA, SoNA
- TLX_RTLX
- TIAS_trust_mean, TIAS_distrust_mean, TIAS_total_trust
- PEmbS_total
