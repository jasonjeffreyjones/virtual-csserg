#!/usr/bin/env python3
"""Render the derivative two-column short report without a TeX runtime."""

from pathlib import Path
import re
from xml.sax.saxutils import escape

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    BalancedColumns,
    BaseDocTemplate,
    Frame,
    Image,
    PageTemplate,
    Paragraph,
    Spacer,
)


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / "website/projects/predict-the-self"
FOREST = colors.HexColor("#18352b")
ARTICHOKE = colors.HexColor("#4b6f44")


def inline(text: str) -> str:
    escaped = escape(text).replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    return re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<a href="\2" color="#4b6f44"><u>\1</u></a>',
        escaped,
    )


def main() -> int:
    output = PUBLIC / "short-report.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)
    width, height = 612, 792
    margin, gap = 42, 20
    document = BaseDocTemplate(
        str(output),
        pagesize=(width, height),
        title="Predict the Self",
        author="Aleph Initial Alpha, Virtual CSSERG",
        subject="Short report on forecasting later self-description",
    )
    frames = [
        Frame(
            margin,
            45,
            width - 2 * margin,
            height - 95,
            id="body",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
    ]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(FOREST)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(margin, 25, "Virtual CSSERG | CC BY 4.0")
        canvas.linkURL(
            "https://creativecommons.org/licenses/by/4.0/", (margin, 20, 150, 34)
        )
        canvas.drawString(170, 25, "Full report | Executive Summary")
        canvas.linkURL(
            "https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/report/",
            (170, 20, 224, 34),
        )
        canvas.linkURL(
            "https://jasonjones.ninja/virtual-csserg/projects/predict-the-self/",
            (229, 20, 315, 34),
        )
        canvas.drawRightString(width - margin, 25, str(doc.page))
        canvas.restoreState()

    document.addPageTemplates(PageTemplate(id="TwoColumns", frames=frames, onPage=footer))
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ReportBody",
            fontName="Helvetica",
            fontSize=8.5,
            leading=10.8,
            spaceAfter=6,
            textColor=FOREST,
            alignment=TA_LEFT,
        )
    )
    styles["Heading1"].fontSize = 17
    styles["Heading1"].leading = 20
    styles["Heading1"].textColor = FOREST
    styles["Heading2"].fontSize = 11
    styles["Heading2"].leading = 14
    styles["Heading2"].textColor = ARTICHOKE
    styles["Heading2"].spaceBefore = 7
    styles["Heading2"].spaceAfter = 5

    logo = ROOT / "website/images/csserg-transparent-logo.png"
    story = [Image(str(logo), width=31, height=35, hAlign="LEFT"), Spacer(1, 7)]
    source = (PROJECT / "short-report.md").read_text(encoding="utf-8")
    for block in source.strip().split("\n\n"):
        block = block.strip()
        style = styles["ReportBody"]
        if block.startswith("# "):
            style, block = styles["Heading1"], block[2:]
        elif block.startswith("## "):
            style, block = styles["Heading2"], block[3:]
        story.append(Paragraph(inline(block).replace("\n", "<br/>"), style))

    document.build(
        [
            BalancedColumns(
                story,
                nCols=2,
                leftPadding=0,
                innerPadding=gap,
                rightPadding=0,
                topPadding=0,
                bottomPadding=0,
            )
        ]
    )
    pages = PdfReader(output).pages
    if not 1 <= len(pages) <= 10:
        raise RuntimeError(f"short report has {len(pages)} pages; expected 1-10")
    if not all(page.extract_text().strip() for page in pages):
        raise RuntimeError("short report contains an empty page")
    print(f"{output.name}: {len(pages)} pages, two-column page template")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
