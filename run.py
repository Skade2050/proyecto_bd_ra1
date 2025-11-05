# run.py
from pathlib import Path
from project.xlsx_export import build_xlsx_from_csv
from project.ingest import read_xlsx_exports
from project.clean import clean_data
from project.store import save_to_sqlite, save_table_sqlite, save_parquet
from project.report import generate_report, export_quality_report

if __name__ == "__main__":
    # 0) GENERAR XLSX SIEMPRE DESDE CSV (origen único)
    csv_dir = Path("data/drops")
    if csv_dir.exists():
        for csv_file in csv_dir.rglob("*.csv"):
            try:
                xlsx_path = build_xlsx_from_csv(str(csv_file))  # crea project/output/xlsx/<nombre>.xlsx
                print(f"[XLSX] Generado: {xlsx_path}")
            except Exception as e:
                print(f"[XLSX] ERROR con {csv_file.name}: {e}")
    else:
        print("AVISO: No existe data/drops; si no hay XLSX exportados, la ingesta fallará.")

    # 1) RAW desde XLSX exportados (SIEMPRE)
    df_raw = read_xlsx_exports("project/output/xlsx")
    save_to_sqlite(df_raw, table="raw_encuestas")

    # 2) CLEAN
    df_clean, df_quarantine = clean_data(df_raw)
    save_table_sqlite(df_clean, table="clean_encuestas")
    save_table_sqlite(df_quarantine, table="quarantine_encuestas")

    # 3) Parquet limpio + Reporte + Informe de calidad (extra)
    save_parquet(df_clean, "project/output/clean_encuestas.parquet")
    generate_report(df_clean, df_quarantine, "project/output/reporte.md")
    export_quality_report(df_clean, df_quarantine, "project/output/informe_de_calidad.xlsx")

    print("Pipeline (CSV -> XLSX exportado) -> RAW -> CLEAN -> Reporte ✅")
