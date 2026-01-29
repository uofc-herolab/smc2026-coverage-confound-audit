#!/usr/bin/env bash
set -euo pipefail

# activate venv if it exists
if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

OUT="deliverables/week01"
mkdir -p "$OUT/paper_cards" "$OUT/memos"

# Build paper card PDFs
for f in paper_cards/*.md; do
  base="$(basename "$f" .md)"
  ./scripts/md_to_pdf.py "$f" "$OUT/paper_cards/${base}.pdf"
done

# Build spine memo PDF
./scripts/md_to_pdf.py memos/j3_spine_memo_v1.md "$OUT/memos/j3_spine_memo_v1.pdf"

echo "Built Week 1 PDFs into: $OUT/"
