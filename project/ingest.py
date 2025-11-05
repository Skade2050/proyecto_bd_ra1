# project/ingest.py
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import pandas as pd

# Columnas “canónicas” mínimas que queremos en raw (si no están, se crean a NaN)
RAW_COLS = [
    "fecha", "id_respuesta", "canal", "producto",
    "satisfaccion", "comentario", "tienda", "agente"
]

def read_xlsx_exports(xlsx_root: str = "project/output/xlsx") -> pd.DataFrame:
    
    root = Path(xlsx_root)
    if not root.exists():
        raise FileNotFoundError(f"No existe la carpeta de exportados XLSX: {xlsx_root}")

    files = [f for f in root.rglob("*.xlsx") if not f.name.startswith("~$")]
    if not files:
        raise FileNotFoundError(f"No se encontraron XLSX exportados en {xlsx_root}")

    frames = []
    now_iso = datetime.now().isoformat()
    for f in files:
        df = pd.read_excel(f, engine="openpyxl")
        # normaliza nombres a minúsculas y sin espacios
        df.columns = [str(c).strip().lower() for c in df.columns]

        # asegura columnas mínimas
        for col in RAW_COLS:
            if col not in df.columns:
                df[col] = pd.NA

        # reordena columnas mínimas al frente
        df = df[RAW_COLS + [c for c in df.columns if c not in RAW_COLS]]

        # trazabilidad
        df["_source_file"] = f.name
        df["_ingest_ts"] = now_iso
        df["_batch_id"] = f.stem  # p.ej. encuestas_202511

        frames.append(df)

    return pd.concat(frames, ignore_index=True)
