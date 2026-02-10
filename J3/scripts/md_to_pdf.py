#!/usr/bin/env python3
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.units import inch

def md_lines_to_flowables(md_text: str):
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], spaceAfter=12)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], spaceAfter=8)
    body = ParagraphStyle("Body", parent=styles["BodyText"], leading=14, spaceAfter=6)

    flow = []
    in_code = False
    code_buf = []

    for raw in md_text.splitlines():
        line = raw.rstrip("\n")

        # code fences
        if line.strip().startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                flow.append(Preformatted("\n".join(code_buf), styles["Code"]))
                flow.append(Spacer(1, 0.1 * inch))
            continue

        if in_code:
            code_buf.append(line)
            continue

        if line.startswith("# "):
            flow.append(Paragraph(line[2:].strip(), h1))
        elif line.startswith("## "):
            flow.append(Paragraph(line[3:].strip(), h2))
        elif line.strip().startswith("- "):
            # simple bullet
            txt = line.strip()[2:].strip()
            flow.append(Paragraph(f"• {txt}", body))
        elif line.strip() == "":
            flow.append(Spacer(1, 0.12 * inch))
        else:
            # Escape minimal HTML chars
            safe = (line.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"))
            flow.append(Paragraph(safe, body))

    # flush unterminated code fence
    if in_code and code_buf:
        flow.append(Preformatted("\n".join(code_buf), styles["Code"]))

    return flow

def main():
    if len(sys.argv) != 3:
        print("Usage: md_to_pdf.py INPUT.md OUTPUT.pdf", file=sys.stderr)
        sys.exit(2)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = in_path.read_text(encoding="utf-8")
    doc = SimpleDocTemplate(str(out_path), pagesize=letter,
                            leftMargin=0.85*inch, rightMargin=0.85*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    flow = md_lines_to_flowables(md_text)
    doc.build(flow)

if __name__ == "__main__":
    main()
