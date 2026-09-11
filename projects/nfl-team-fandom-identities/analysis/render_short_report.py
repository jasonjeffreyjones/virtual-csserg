#!/usr/bin/env python3
"""Render the derivative short report with two columns; no TeX runtime needed.

Requires the optional publication packages in requirements-publication.txt.
The intentionally small Markdown subset is headings, paragraphs, images, links.
"""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Image, Spacer, PageBreak, FrameBreak
from pypdf import PdfReader

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PUBLIC = ROOT / 'website/projects/nfl-team-fandom-identities'
FOREST = colors.HexColor('#18352b')


def inline(text):
    text = escape(text).replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")
    return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" color="#4b6f44">\1</a>', text)


def main():
    output = PUBLIC / 'short-report.pdf'
    width, height = 612, 792
    margin, gap = 42, 20
    column = (width - 2 * margin - gap) / 2
    doc = BaseDocTemplate(str(output), pagesize=(width, height),
                          title='Happy endorsement and Cleveland Browns fandom',
                          author='Ceetown and Aleph Initial Alpha, Virtual CSSERG')
    frames = [Frame(margin + i*(column+gap), 45, column, height-95,
                    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
              for i in range(2)]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(FOREST)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(margin, 25, 'Virtual CSSERG | CC BY 4.0')
        canvas.linkURL('https://creativecommons.org/licenses/by/4.0/', (margin, 22, 200, 34))
        canvas.drawString(220, 25, 'Dr. Jason Jeffrey Jones | CSSERG')
        canvas.linkURL('https://jasonjones.ninja/', (220, 22, 303, 34))
        canvas.linkURL('https://jasonjones.ninja/csserg/', (308, 22, 350, 34))
        canvas.drawRightString(width-margin, 25, str(doc.page))
        canvas.restoreState()

    doc.addPageTemplates(PageTemplate(id='TwoColumns', frames=frames, onPage=footer))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Body', fontName='Helvetica', fontSize=9.5,
                              leading=12.2, spaceAfter=7, textColor=FOREST, alignment=TA_LEFT))
    styles['Heading1'].fontSize = 17
    styles['Heading1'].leading = 20
    styles['Heading1'].textColor = FOREST
    styles['Heading2'].fontSize = 11
    styles['Heading2'].leading = 14
    styles['Heading2'].textColor = FOREST
    logo = ROOT / 'website/images/csserg-transparent-logo.png'
    story = [Image(str(logo), width=34, height=38, hAlign='LEFT'), Spacer(1, 8)]
    for block in (PROJECT/'short-report.md').read_text().strip().split('\n\n'):
        block = block.strip()
        if block == '## Sensitivity checks':
            story.append(PageBreak())
        if block == '## References':
            story.append(FrameBreak())
        if block.startswith('!['):
            path = re.search(r'\]\(([^)]+)\)', block).group(1)
            story.extend([Image(str(PUBLIC/path), width=column, height=column*1000/1600), Spacer(1, 8)])
        else:
            style = styles['Body']
            if block.startswith('# '):
                style, block = styles['Heading1'], block[2:]
            elif block.startswith('## '):
                style, block = styles['Heading2'], block[3:]
            story.append(Paragraph(inline(block).replace('\n', '<br/>'), style))
    doc.build(story)
    pages = PdfReader(output).pages
    assert len(pages) <= 10, f'Short report exceeds 10 pages: {len(pages)}'
    assert all(page.extract_text().strip() for page in pages)
    print(f'{output.name}: {len(pages)} pages, two columns')


if __name__ == '__main__':
    main()
