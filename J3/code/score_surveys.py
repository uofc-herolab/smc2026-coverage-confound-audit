#!/usr/bin/env python3
"""
score_surveys.py
Reads a CSV export of survey responses and writes a scored CSV.

Expected input columns (minimum recommended):
IDs:
- subject_id, session_id, block_id, condition

SoAS:
- sopa_*  (SoPA items)
- sona_*  (SoNA items)

NASA-TLX:
- tlx_mental, tlx_physical, tlx_temporal, tlx_performance, tlx_effort, tlx_frustration

Trust (TIAS / Jian 2000 recommended naming):
- tias_trust_*    (trust items)
- tias_distrust_* (distrust items, reverse-coded for total trust)

Embodiment (PEmbS):
- pembs_01 .. pembs_10

Notes:
- We do not hardcode item counts. The script averages whatever item columns exist.
- Missing/blank values are ignored.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Optional


def _to_float(x: str) -> Optional[float]:
    x = (x or "").strip()
    if x == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def mean_ignore_missing(values: List[Optional[float]]) -> Optional[float]:
    nums = [v for v in values if v is not None]
    if not nums:
        return None
    return sum(nums) / len(nums)


def cols_with_prefix(row: Dict[str, str], prefix: str) -> List[str]:
    return sorted([k for k in row.keys() if k.startswith(prefix)])


def reverse_1_to_7(x: float) -> float:
    # For a 1..7 Likert item, reverse coding is: 8 - x
    return 8.0 - x


def score_row(row: Dict[str, str]) -> Dict[str, str]:
    out: Dict[str, str] = {}

    # IDs (pass-through)
    for k in ["subject_id", "session_id", "block_id", "condition"]:
        if k in row:
            out[k] = row[k]

    # -------------------------
    # SoAS: SoPA / SoNA
    # -------------------------
    sopa_cols = cols_with_prefix(row, "sopa_")
    sona_cols = cols_with_prefix(row, "sona_")
    sopa = mean_ignore_missing([_to_float(row.get(c, "")) for c in sopa_cols])
    sona = mean_ignore_missing([_to_float(row.get(c, "")) for c in sona_cols])
    out["SoPA"] = "" if sopa is None else f"{sopa:.4f}"
    out["SoNA"] = "" if sona is None else f"{sona:.4f}"

    # Optional quick rating
    abr = _to_float(row.get("agency_block_rating", ""))
    out["agency_block_rating"] = "" if abr is None else f"{abr:.4f}"

    # -------------------------
    # NASA-TLX (Raw TLX)
    # -------------------------
    tlx_keys = [
        "tlx_mental",
        "tlx_physical",
        "tlx_temporal",
        "tlx_performance",
        "tlx_effort",
        "tlx_frustration",
    ]
    tlx_vals = [_to_float(row.get(k, "")) for k in tlx_keys]
    tlx_rtlx = mean_ignore_missing(tlx_vals)
    out["TLX_RTLX"] = "" if tlx_rtlx is None else f"{tlx_rtlx:.4f}"

    # -------------------------
    # Trust: TIAS (Jian 2000)
    # -------------------------
    trust_cols = cols_with_prefix(row, "tias_trust_")
    distrust_cols = cols_with_prefix(row, "tias_distrust_")

    trust_vals = [_to_float(row.get(c, "")) for c in trust_cols]
    distrust_vals = [_to_float(row.get(c, "")) for c in distrust_cols]

    trust_mean = mean_ignore_missing(trust_vals)
    distrust_mean = mean_ignore_missing(distrust_vals)

    out["TIAS_trust_mean"] = "" if trust_mean is None else f"{trust_mean:.4f}"
    out["TIAS_distrust_mean"] = "" if distrust_mean is None else f"{distrust_mean:.4f}"

    # Total trust: trust items + reversed distrust items
    combined: List[Optional[float]] = []
    combined.extend(trust_vals)
    combined.extend([None if v is None else reverse_1_to_7(v) for v in distrust_vals])
    total_trust = mean_ignore_missing(combined)
    out["TIAS_total_trust"] = "" if total_trust is None else f"{total_trust:.4f}"

    # -------------------------
    # Embodiment: PEmbS total
    # -------------------------
    pembs_cols = cols_with_prefix(row, "pembs_")
    pembs_vals = [_to_float(row.get(c, "")) for c in pembs_cols]
    pembs_total = mean_ignore_missing(pembs_vals)
    out["PEmbS_total"] = "" if pembs_total is None else f"{pembs_total:.4f}"

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_csv", required=True, help="Input CSV export from surveys")
    ap.add_argument("--out_csv", required=True, help="Output scored CSV")
    args = ap.parse_args()

    in_path = Path(args.in_csv)
    out_path = Path(args.out_csv)

    if not in_path.exists():
        raise SystemExit(f"Input not found: {in_path}")

    with in_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    scored_rows = [score_row(r) for r in rows]

    # Stable column order: accumulate keys in encounter order
    fieldnames: List[str] = []
    for r in scored_rows:
        for k in r.keys():
            if k not in fieldnames:
                fieldnames.append(k)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(scored_rows)

    print(f"✅ Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
