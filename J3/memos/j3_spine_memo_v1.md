# J3 Spine Memo v1

## One-sentence thesis
J3 validates that **agency-constrained shared autonomy** can help prosthetic grasp selection **without making users feel overridden**, by linking objective controller logs (ALI, τ) to validated agency and workload measures.

## What J3 must prove
- Validity: ALI ↔ SoAS
- Constraint benefit: constrained arbitration vs blending preserves agency/trust at comparable performance
- AugCog: adaptive τ(t) reduces workload when demand is high without harming agency

## Hypotheses (draft)
- H1: ALI correlates with SoAS (SoPA/SoNA) during hardware interaction.
- H2: SetACSA (fixed τ) preserves agency better than confidence blending at similar performance.
- H3: CS-AAB / CSAAB (adaptive τ(t)) reduces workload (NASA-TLX + pupil proxy) during high-demand segments without degrading agency.

## Key variables (draft)
Logged: p_u(g), p_a(g), g_exec, c_u, H(p_u), ALI(g_exec), τ or τ(t)  
Measured: SoAS (SoPA/SoNA), NASA-TLX (total + subscales), pupil workload proxy, task success/time/errors

## Novelty statement (10 lines)
1) J3 validates controller-side agency loss with human subjective agency measures, not offline proxies.
2) J3 compares constrained arbitration against blending with human outcomes.
3) J3 tests workload-adaptive τ(t) using pupillometry + uncertainty signals.
4) J3 uses SoPA/SoNA to capture agency–performance decoupling.
5) J3 uses TLX subscales to diagnose workload/frustration drivers.
6) J3 enforces pupil/EMG preprocessing SOPs to avoid artifact-driven conclusions.
7) J3 includes transparency/trust framing to reduce surprise autonomy confounds.
8) J3 yields auditable logs linking controller decisions to human outcomes.
9) J3 bridges benchmark shared control results to agency-preserving constraints.
10) J3 creates reusable artifacts for downstream engineering and translation.

## Biggest risks + mitigations
- Performance confound in agency → include covariates; separate SoPA vs SoNA
- Luminance confound in pupil → strict lighting SOP + baseline correction + QC
- Probability miscalibration → calibrate p_u before ALI/entropy/τ(t)
- Transparency overload → minimal cues; monitor TLX mental demand/frustration
