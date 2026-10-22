"""Convierte un archivo Markdown a PDF usando markdown + xhtml2pdf (100% Python).

Uso:
    python tools/md_to_pdf.py <entrada.md> <salida.pdf> [--cover <cover.html>] [--apa]

Opciones:
    --cover <archivo.html>  Antepone una portada (HTML) antes del contenido.
    --apa                   Aplica formato APA 7 (Carta, margenes 1in, Times 12pt,
                            interlineado doble, numero de pagina arriba a la derecha).
"""
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

# Reemplazos de simbolos sin glifo en las fuentes base del PDF.
_REPL = {
    "⚠️": "[Aviso]",
    "⚠": "[Aviso]",
    "✅": "[OK]",
    "⏳": "[Pendiente]",
    "\U0001f3af": "",
    "→": "->",
    "≤": "<=",
    "≥": ">=",
    "×": "x",
}

# Estilo base (no APA).
CSS_BASE = """
@page { size: A4; margin: 2cm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10pt; color: #1f2a37; line-height: 1.4; }
h1 { font-size: 20pt; color: #0b5394; }
h2 { font-size: 15pt; color: #0b5394; border-bottom: 1px solid #c7cfd8; padding-bottom: 3px; margin-top: 18px; }
h3 { font-size: 12pt; color: #09426f; }
table { width: 100%; margin: 8px 0; }
th, td { border: 1px solid #c7cfd8; padding: 4px 6px; text-align: left; font-size: 9pt; }
th { background-color: #f0f3f6; }
code, pre { font-family: Courier, monospace; font-size: 8.5pt; background-color: #f4f6f8; }
pre { padding: 6px; border: 1px solid #e3e8ee; }
.page-break { page-break-after: always; }
"""

# Estilo APA 7 (version estudiante): Carta, 1in, Times 12, interlineado doble,
# numero de pagina arriba a la derecha. Tablas y codigo a espacio simple por
# legibilidad (APA permite espacio simple en tablas).
CSS_APA = """
@page {
  size: letter;
  margin: 1in;
  @frame header_frame { -pdf-frame-content: headerContent; top: 0.5in; left: 1in; width: 6.5in; height: 0.3in; }
}
body { font-family: "Times New Roman", Times, serif; font-size: 12pt; color: #000000; line-height: 2.0; }
h1 { font-size: 14pt; color: #000000; text-align: center; }
h2 { font-size: 12pt; color: #000000; font-weight: bold; margin-top: 14px; }
h3 { font-size: 12pt; color: #000000; font-weight: bold; font-style: italic; }
p, li { line-height: 2.0; text-align: justify; }
table { width: 100%; margin: 8px 0; }
th, td { border: 1px solid #000000; padding: 3px 5px; text-align: left; font-size: 10pt; line-height: 1.1; }
th { background-color: #e9e9e9; font-weight: bold; }
code, pre { font-family: Courier, monospace; font-size: 9pt; line-height: 1.1; background-color: #f2f2f2; }
pre { padding: 6px; border: 1px solid #cccccc; }
.page-break { page-break-after: always; }

/* Portada APA */
.apa-cover { text-align: center; }
.apa-top-gap { height: 2.2in; }
.apa-title { font-size: 12pt; line-height: 2.0; margin: 0; }
.apa-line { font-size: 12pt; line-height: 2.0; margin: 0; }
.apa-gap { height: 0.5in; }
.apa-gap-small { height: 0.25in; }
"""

# Encabezado con numero de pagina (arriba a la derecha), repetido en cada pagina.
HEADER_HTML = (
    '<div id="headerContent" style="text-align:right; font-family:Times; font-size:12pt;">'
    '<pdf:pagenumber></div>'
)


def main() -> int:
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2

    src = Path(args[0])
    dst = Path(args[1])
    cover_path = None
    apa = False
    i = 2
    while i < len(args):
        if args[i] == "--cover" and i + 1 < len(args):
            cover_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--apa":
            apa = True
            i += 1
        else:
            print(f"Argumento no reconocido: {args[i]}")
            return 2

    text = src.read_text(encoding="utf-8")
    for a, b in _REPL.items():
        text = text.replace(a, b)

    body = markdown.markdown(
        text, extensions=["tables", "fenced_code", "toc", "sane_lists"]
    )

    cover_html = ""
    if cover_path and cover_path.exists():
        cover_html = cover_path.read_text(encoding="utf-8")

    css = CSS_APA if apa else CSS_BASE
    header = HEADER_HTML if apa else ""

    html = (
        f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>"
        f"{header}{cover_html}{body}</body></html>"
    )

    with dst.open("wb") as out:
        result = pisa.CreatePDF(html, dest=out, encoding="utf-8")

    if result.err:
        print(f"ERROR: la conversion produjo {result.err} error(es).")
        return 1
    print(f"PDF generado: {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
