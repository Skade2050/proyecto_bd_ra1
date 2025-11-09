# tools/copy_report_to_site.py
from pathlib import Path
import shutil

SRC = Path("project/output/reporte.md")
DST = Path("site/content/reports/reporte-encuestas.md")
DST.parent.mkdir(parents=True, exist_ok=True)

if not SRC.exists():
    raise SystemExit("No existe project/output/reporte.md. Ejecuta el pipeline primero.")

# opcional: añade frontmatter si no lo trae
tmp = DST.with_suffix(".tmp")
text = SRC.read_text(encoding="utf-8")
if not text.lstrip().startswith("---"):
    text = f"---\ntitle: Reporte de Encuestas\n---\n\n" + text
tmp.write_text(text, encoding="utf-8")
shutil.move(tmp, DST)
print(f"Copiado a {DST}")
