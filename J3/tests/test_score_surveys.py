import csv
import subprocess
from pathlib import Path

def test_score_surveys_runs(tmp_path: Path):
    repo = Path(__file__).resolve().parents[1]
    in_csv = repo / "tests" / "dummy_responses.csv"
    out_csv = tmp_path / "scores.csv"

    cmd = [str(repo / "code" / "score_surveys.py"), "--in_csv", str(in_csv), "--out_csv", str(out_csv)]
    subprocess.check_call(cmd)

    assert out_csv.exists()

    with out_csv.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2

    # Check expected columns exist
    for k in ["SoPA", "SoNA", "TLX_RTLX", "TIAS_trust_mean", "TIAS_distrust_mean", "TIAS_total_trust", "PEmbS_total"]:
        assert k in rows[0], f"missing column: {k}"

    # Row 1 expectations (formatted to 4 decimals)
    assert rows[0]["SoPA"] == "6.5000"
    assert rows[0]["SoNA"] == "1.5000"
    assert rows[0]["TLX_RTLX"] == "35.0000"
    assert rows[0]["TIAS_trust_mean"] == "6.0000"
    assert rows[0]["TIAS_distrust_mean"] == "2.0000"
    assert rows[0]["TIAS_total_trust"] == "6.0000"
    assert rows[0]["PEmbS_total"] == "2.0000"

    # Row 2 expectations
    assert rows[1]["SoPA"] == "5.5000"
    assert rows[1]["SoNA"] == "2.5000"
    assert rows[1]["TLX_RTLX"] == "45.0000"
    assert rows[1]["TIAS_trust_mean"] == "5.0000"
    assert rows[1]["TIAS_distrust_mean"] == "3.0000"
    assert rows[1]["TIAS_total_trust"] == "5.0000"
    assert rows[1]["PEmbS_total"] == "1.0000"
