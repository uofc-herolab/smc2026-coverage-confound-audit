#!/usr/bin/env python3
"""
score_surveys.py
Reads a CSV export of survey responses and writes a scored CSV.

Assumes the CSV has:
- IDs: subject_id, session_id, block_id, condition
- SoAS item columns prefixed with: sopa_ , sona_
- TLX subscales: tlx_mental, tlx_physical, tlx_temporal, tlx_performance, tlx_effort, tlx_frustration
- Optional: trust_*, embod_*, agency_block_rating
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple


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


def score_row(row: Dict[str, str]) -> Dict[str, str]:
    out: Dict[str, str] = {}

    # IDs (pass-through if present)
    for k in ["subject_id", "session_id", "block_id", "condition"]:
        if k in row:
            out[k] = row[k]

    # SoAS
    sopa_cols = cols_with_prefix(row, "sopa_")
    sona_cols = cols_with_prefix(row, "sona_")

    sopa_vals = [_to_float(row.get(c, "")) for c in sopa_cols]
    sona_vals = [_to_float(row.get(c, "")) for c in sona_cols]

    sopa = mean_ignore_missing(sopa_vals)
    sona = mean_ignore_missing(sona_vals)

    out["SoPA"] = "" if sopa is None else f"{sopa:.4f}"
    out["SoNA"] = "" if sona is None else f"{sona:.4f}"

    # Quick per-block agency rating (0-100)
    abr = _to_float(row.get("agency_block_rating", ""))
    out["agency_block_rating"] = "" if abr is None else f"{abr:.4f}"

    # NASA-TLX (Raw TLX)
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

    # Trust + Embodiment (optional, mean of prefixes)
    trust_cols = cols_with_prefix(row, "trust_")
    embod_cols = cols_with_prefix(row, "embod_")

    trust = mean_ignore_missing([_to_float(row.get(c, "")) for c in trust_cols])
    embod = mean_ignore_missing([_to_float(row.get(c, "")) for c in embod_cols])

    out["trust_mean"] = "" if trust is None else f"{trust:.4f}"
    out["embod_mean"] = "" if embod is None else f"{embod:.4f}"

    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in_csv", required=True, help="Input CSV export from forms/qualtrics")
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
    # union of keys, stable order
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
