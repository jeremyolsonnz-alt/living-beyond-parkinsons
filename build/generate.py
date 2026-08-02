#!/usr/bin/env python3
"""
Living Beyond Parkinson's — single-source script generator.

One JSON per practice (build/scripts/<id>.json) is the single source of truth.
Each paragraph has an 'agnostic' rendering (the default wording, and the audio
narration) plus optional 'see' / 'feel' overrides used by the on-page toggle
and the printable versions.

From each JSON this produces, into build/out/:
  audio/<id>.txt              - agnostic narration script (for Jeremy to record directly)
  print/<id>-both.html        - print-ready, agnostic wording
  print/<id>-see.html         - print-ready, 'seeing' wording
  print/<id>-feel.html        - print-ready, 'feeling' wording
  partials/<id>.script.html   - injectable script block with data-see/data-feel
                                attributes (agnostic is the default text)

The print HTML is styled for A4 and can be turned into PDF by any browser's
"Print to PDF" or by wkhtmltopdf / weasyprint. No third-party packages needed
to run this generator.

Usage:
    python3 generate.py                # build every scripts/*.json
    python3 generate.py walking-freely # build one
"""

import html
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
SCRIPTS = BASE / "scripts"
OUT = BASE / "out"

MODES = ("both", "see", "feel")
# 'both' uses the agnostic wording (serves seeing and feeling from the same words).
MODE_KEY = {"both": "agnostic", "see": "see", "feel": "feel"}
MODE_LABEL = {
    "both": "Seeing and feeling (default wording)",
    "see": "For people who imagine by seeing",
    "feel": "For people who imagine by feeling",
}


def rendering(paragraph, mode):
    """Return the paragraph text for a mode, falling back to agnostic."""
    key = MODE_KEY[mode]
    return paragraph.get(key) or paragraph["agnostic"]


# ---------------------------------------------------------------------------
# 1. Audio narration script (agnostic only)
# ---------------------------------------------------------------------------
def build_audio(data):
    lines = [
        data["title"].upper(),
        "Guided imagery narration — agnostic wording",
        f"(approx. {data['approx_minutes']} minutes)",
        "",
        "Narrator note: read slowly, permissively, with long pauses at each",
        "paragraph break. Nothing here is a command; every line is an invitation.",
        "",
    ]
    for phase in data["phases"]:
        lines.append(f"[{phase['label'].upper()}]")
        lines.append("")
        for para in phase["paragraphs"]:
            lines.append(para["agnostic"])
            lines.append("")   # blank line = pause
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# 2. Print-ready HTML (one per mode) -> PDF via browser / wkhtmltopdf
# ---------------------------------------------------------------------------
PRINT_CSS = """
@page { size: A4; margin: 22mm 20mm; }
* { box-sizing: border-box; }
body { font-family: Georgia, 'Times New Roman', serif; color: #2A2820;
       line-height: 1.6; font-size: 12pt; }
.head { border-bottom: 2px solid #C8963C; padding-bottom: 10px; margin-bottom: 22px; }
.brand { font-size: 10pt; letter-spacing: .12em; text-transform: uppercase;
         color: #C8963C; }
h1 { font-size: 22pt; margin: 6px 0 2px; }
.mode { font-size: 10pt; color: #7A7060; font-style: italic; }
.phase { margin-top: 20px; }
.phase h2 { font-size: 13pt; color: #5C4A2A; border-bottom: 1px solid #E0D8C8;
            padding-bottom: 4px; margin-bottom: 10px; page-break-after: avoid; }
p { margin: 0 0 12px; }
.foot { margin-top: 26px; padding-top: 12px; border-top: 1px solid #E0D8C8;
        font-size: 9.5pt; color: #7A7060; }
"""


def build_print(data, mode):
    title = html.escape(data["title"])
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>",
        f"<title>{title} — {MODE_LABEL[mode]}</title>",
        f"<style>{PRINT_CSS}</style></head><body>",
        "<div class='head'>",
        "<div class='brand'>Living Beyond Parkinson's · Guided Imagery</div>",
        f"<h1>{title}</h1>",
        f"<div class='mode'>{html.escape(MODE_LABEL[mode])}</div>",
        "</div>",
    ]
    for phase in data["phases"]:
        parts.append("<div class='phase'>")
        parts.append(f"<h2>{html.escape(phase['label'])}</h2>")
        for para in phase["paragraphs"]:
            parts.append(f"<p>{html.escape(rendering(para, mode))}</p>")
        parts.append("</div>")
    parts.append(
        "<div class='foot'>This four-part structure is the author's own "
        "synthesis, not a clinically tested unified protocol. It is a complement "
        "to medical care, physiotherapy and cueing strategies — never a "
        "replacement. Free to print and share.</div>"
    )
    parts.append("</body></html>")
    return "".join(parts)


# ---------------------------------------------------------------------------
# 3. Injectable script partial with data-see / data-feel attributes
# ---------------------------------------------------------------------------
def build_partial(data):
    """
    Emits the <details> script blocks used inside the practice page.
    Paragraphs that have see/feel overrides carry data-see and data-feel so the
    toggle JS can swap their text; the default (visible) text is the agnostic
    wording. Paragraphs with no overrides are static.
    """
    out = ["<!-- AUTO-GENERATED from build/scripts/%s.json — do not edit by hand -->"
           % data["id"]]
    first = True
    for phase in data["phases"]:
        open_attr = " open" if first else ""
        first = False
        marker = "·" if phase["id"] in ("opening", "closing") else \
                 ("I" if phase["id"] == "phase1" else "II")
        out.append(f'<details class="script"{open_attr}>')
        out.append(
            '  <summary><span class="phase-no">%s</span>'
            '<span class="phase-name">%s</span>'
            '<span class="chev">&#9656;</span></summary>'
            % (marker, html.escape(phase["label"]))
        )
        out.append('  <div class="script-body">')
        for para in phase["paragraphs"]:
            agnostic = html.escape(para["agnostic"])
            attrs = ""
            if "see" in para:
                attrs += ' data-see="%s"' % html.escape(para["see"], quote=True)
            if "feel" in para:
                attrs += ' data-feel="%s"' % html.escape(para["feel"], quote=True)
            if attrs:
                attrs += ' data-agnostic="%s"' % html.escape(para["agnostic"], quote=True)
            out.append(f'    <p{attrs}>{agnostic}</p>')
        out.append('  </div>')
        out.append('</details>')
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
def build_one(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    pid = data["id"]

    (OUT / "audio").mkdir(parents=True, exist_ok=True)
    (OUT / "print").mkdir(parents=True, exist_ok=True)
    (OUT / "partials").mkdir(parents=True, exist_ok=True)

    (OUT / "audio" / f"{pid}.txt").write_text(build_audio(data), encoding="utf-8")
    for mode in MODES:
        (OUT / "print" / f"{pid}-{mode}.html").write_text(
            build_print(data, mode), encoding="utf-8")
    (OUT / "partials" / f"{pid}.script.html").write_text(
        build_partial(data), encoding="utf-8")

    written = [f"audio/{pid}.txt"] + [f"print/{pid}-{m}.html" for m in MODES] + \
              [f"partials/{pid}.script.html"]
    return written


def main(argv):
    if argv:
        targets = [SCRIPTS / f"{a.replace('.json','')}.json" for a in argv]
    else:
        targets = sorted(SCRIPTS.glob("*.json"))
    if not targets:
        print("No script JSON files found in", SCRIPTS)
        return 1
    for path in targets:
        if not path.exists():
            print("  missing:", path.name)
            continue
        written = build_one(path)
        print(f"built {path.name} ->")
        for w in written:
            print(f"    out/{w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
