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
    assert "SoPA" in rows[0]
    assert "SoNA" in rows[0]
    assert "TLX_RTLX" in rows[0]
