#!/usr/bin/env python3
"""
audit_feature_table.py

Reads a feature table and prints dataset summary stats to verify what you report in the paper.
Supported formats: .csv, .parquet, .feather

It prints:
- total rows
- unique subjects
- label value counts (and binary prevalence when applicable)
- Cov3 summary stats (if columns exist)
- optional fold leakage check (if you have a fold column)
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

import pandas as pd

SUPPORTED = {".csv", ".parquet", ".feather"}

def read_table(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path)
    if ext == ".parquet":
        return pd.read_parquet(path)
    if ext == ".feather":
        return pd.read_feather(path)
    raise SystemExit(f"Unsupported extension {ext}. Supported: {', '.join(sorted(SUPPORTED))}")

def header(title: str) -> None:
    print("\n" + "=" * len(title))
    print(title)
    print("=" * len(title))

def summarize_label(df: pd.DataFrame, col: str) -> None:
    if col not in df.columns:
        print(f"- {col}: NOT FOUND")
        return
    s = df[col]
    vc = s.value_counts(dropna=False)

    print(f"- {col}: missing={int(s.isna().sum()):,}, unique={int(s.nunique(dropna=True)):,}")
    for i, (val, cnt) in enumerate(vc.items()):
        if i >= 12:
            remaining = len(vc) - 12
            if remaining > 0:
                print(f"  ... ({remaining} more values)")
            break
        print(f"  {repr(val)}: {int(cnt):,}")

    # If binary 0/1 or True/False, compute prevalence (no assumptions beyond that)
    non_na = s.dropna()
    if non_na.empty:
        return
    vals = set(non_na.unique().tolist())
    if vals.issubset({0, 1}):
        pos = int((non_na == 1).sum())
        neg = int((non_na == 0).sum())
        prev = pos / (pos + neg) if (pos + neg) else float("nan")
        print(f"  binary summary: pos(1)={pos:,}, neg(0)={neg:,}, prevalence={prev:.4f}")
    elif vals.issubset({False, True}):
        pos = int((non_na == True).sum())   # noqa: E712
        neg = int((non_na == False).sum())  # noqa: E712
        prev = pos / (pos + neg) if (pos + neg) else float("nan")
        print(f"  binary summary: pos(True)={pos:,}, neg(False)={neg:,}, prevalence={prev:.4f}")

def summarize_cov3(df: pd.DataFrame, cov3_cols: List[str]) -> None:
    ok = [c for c in cov3_cols if c in df.columns]
    missing = [c for c in cov3_cols if c not in df.columns]
    if missing:
        print(f"Cov3 columns missing (skipping): {missing}")
    if not ok:
        return

    desc = df[ok].describe(percentiles=[0.25, 0.5, 0.75]).T
    keep = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    desc = desc[keep]
    print(desc.to_string(float_format=lambda x: f"{x:.4g}"))

def fold_leakage_check(df: pd.DataFrame, subject_col: str, fold_col: str) -> None:
    if subject_col not in df.columns:
        print(f"Cannot check folds: subject_col '{subject_col}' not found.")
        return
    if fold_col not in df.columns:
        print(f"Cannot check folds: fold_col '{fold_col}' not found.")
        return

    tmp = df[[subject_col, fold_col]].dropna().drop_duplicates()
    per_sub = tmp.groupby(subject_col)[fold_col].nunique()
    bad = per_sub[per_sub > 1]

    print(f"fold_col={fold_col}, unique_folds={tmp[fold_col].nunique():,}")
    print(f"subjects appearing in >1 fold: {len(bad):,}")
    if len(bad) > 0:
        print("Example problematic subjects (first 10):")
        print(bad.head(10).to_string())

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True, help="Path to feature table (.csv/.parquet/.feather)")
    ap.add_argument("--name", default="DATASET", help="Name printed in header")
    ap.add_argument("--subject-col", default="subject_id", help="Subject/group id column")
    ap.add_argument("--label-cols", nargs="*", default=["y"], help="One or more label columns to summarize")
    ap.add_argument("--cov3-cols", nargs="*", default=["event_count", "active_hours", "unique_rooms"], help="Cov3 columns")
    ap.add_argument("--fold-col", default=None, help="Optional fold column for leakage check (e.g., fold)")
    ap.add_argument("--list-columns", action="store_true", help="Print all columns and exit")
    args = ap.parse_args()

    df = read_table(args.path)

    header(f"{args.name}: {os.path.basename(args.path)}")
    print(f"rows: {len(df):,}")
    if args.subject_col in df.columns:
        print(f"unique {args.subject_col}: {df[args.subject_col].nunique(dropna=True):,}")
    else:
        print(f"WARNING: subject_col '{args.subject_col}' not found. Use --list-columns to inspect.")

    if args.list_columns:
        print("\nCOLUMNS:")
        for c in df.columns:
            print(c)
        return

    print("\nLABEL DISTRIBUTIONS:")
    for col in args.label_cols:
        summarize_label(df, col)

    print("\nCOV3 SUMMARY (overall):")
    summarize_cov3(df, args.cov3_cols)

    if args.fold_col:
        print("\nFOLD LEAKAGE CHECK:")
        fold_leakage_check(df, args.subject_col, args.fold_col)

if __name__ == "__main__":
    main()
