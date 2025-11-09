---
title: "1. Ingesta y Almacenamiento"
description: "Proceso de carga inicial de datos, trazabilidad y almacenamiento en bruto (capa Bronze)."
---
## Contexto del Proyecto  

El objetivo de este proyecto es construir un **pipeline de datos** que procese las encuestas mensuales recibidas en formato Excel (`*.xlsx`).  
A través de este flujo, los datos crudos se limpian, validan y transforman en información útil para el análisis posterior.  

De esta forma, se asegura que las métricas de satisfacción reflejen **datos fiables y trazables**, garantizando la calidad del análisis mensual.  

---

## Proceso de Ingesta  

El proceso de ingesta comienza con la **recopilación y normalización** de los archivos Excel que contienen las encuestas.

1. ### **Origen de los Datos**  
   - Los datos de entrada se encuentran en la carpeta `project/output/xlsx/`.  
   - Cada archivo (`*.xlsx`) representa un lote mensual de respuestas recogidas.  
   - Estos ficheros contienen información sobre:  
     - `fecha` de la encuesta  
     - `id_respuesta`  
     - `canal` (por ejemplo, online o tienda)  
     - `producto`  
     - `satisfacción` (valor del 1 al 10)  
     - `comentario`, `tienda` y `agente`  

2. ### **Lectura y Normalización**  
   Durante esta fase, el sistema:  
   - **Lee cada Excel** mediante la función `read_xlsx_exports()` (archivo `ingest.py`).  
   - **Estandariza los nombres de las columnas** a minúsculas y elimina espacios en blanco.  
   - **Asegura la existencia** de las columnas mínimas necesarias (`fecha`, `id_respuesta`, `satisfaccion`, etc.).  
   - Añade tres columnas de **trazabilidad**:  
     ```text
     _source_file   → nombre del archivo original  
     _ingest_ts     → fecha y hora exactas en que se procesó el archivo  
     _batch_id      → identificador del lote (por ejemplo, "encuestas_202511")
     ```  

3. ### **Almacenamiento Inicial (Capa Raw)**  
   Una vez procesadas las encuestas, se almacenan en una base de datos SQLite (`project/encuestas.db`), dentro de la tabla `raw_encuestas`.  

   Este paso garantiza que todos los datos originales queden **respaldados** y disponibles para futuras revisiones o reprocesos.  

   Además, también se genera una copia en formato **Parquet** (`clean_encuestas.parquet`) dentro de `project/output/xlsx/`, lo que facilita su uso en herramientas analíticas.

---

## Ejemplo de Flujo  

```text
data/drops/encuestas_2025_large.csv
       ↓
xlsx_export.py  →  genera Excel limpio (Encuestas + ResumenCalidad)
       ↓
ingest.py       →  lee los Excels y los combina en un solo DataFrame
       ↓
store.py        →  guarda los datos en SQLite (raw_encuestas)
       ↓
clean.py        →  limpia y valida los registros
