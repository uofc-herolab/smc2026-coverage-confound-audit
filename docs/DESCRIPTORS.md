# CovPP descriptors and TIHM residualization

## Cov3 (coverage proxies)
1) event_count: total sensor events  
2) active_hours: number of active hours  
3) unique_rooms: count of distinct rooms accessed  

## CovPP added descriptors (9)
1) transition_per_event: number of room transitions divided by event_count  
2–9) room_prop_1 ... room_prop_8: proportion of events occurring in each room (sum to 1)  

## TIHM fold-wise ridge residualization (CovPP)
Within each training fold:
- For each added descriptor z_k in CovPP extras, fit ridge regression:
  z_k ~ Cov3 with alpha = 1.0 (fixed; not tuned)
- Compute residuals:
  z_k_perp = z_k - z_k_hat
- Train classifier on [Cov3, z_perp]
- Apply the same training-fold ridge fit to transform the test fold (prevents leakage)
