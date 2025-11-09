---
title: "3. Modelado y Generación de Reportes"
description: "Transformación de datos validados en información útil mediante KPIs y reportes analíticos automáticos."
---

## Contexto  

Una vez completada la fase de **limpieza**, los datos de encuestas ya son fiables y coherentes.  
El siguiente paso del pipeline consiste en **modelarlos** y **resumirlos** en un formato comprensible para el análisis mensual.  

El objetivo principal de esta etapa es **transformar los datos limpios en información útil**, calculando métricas clave (KPIs) y generando un **reporte en formato Markdown** que sintetiza los resultados del periodo.

---

## 1. Modelado: Transformar Datos Limpios en Métricas  

El modelado se realiza en el archivo `report.py`, a través de la función `generate_report()`.  
Aquí se agrupan y analizan los datos limpios (`clean_encuestas`) para obtener indicadores relevantes:

### **KPIs calculados**
| Métrica | Descripción | Ejemplo |
|:--------|:-------------|:---------|
| **Encuestas (clean)** | Número total de registros válidos tras la limpieza. | 1.838 |
| **NS/NC** | Respuestas sin valoración (nulos o “no sabe/no contesta”). | 227 (12.4%) |
| **Media de satisfacción** | Promedio aritmético de las puntuaciones de satisfacción (1–10). | 5.41 |
| **Evolución mensual** | Cantidad y media de satisfacción por mes. | Enero: 5.43 — Febrero: 5.70 |

Estos valores se calculan agrupando la columna `satisfaccion` y ordenando las fechas por mes.

---

## 2. Estructura del Reporte  

El reporte se genera automáticamente en formato Markdown (`reporte.md`) dentro de la carpeta `project/output/`.  
Contiene cuatro secciones principales:

### 🧾 **1. Contexto**
Información básica sobre los datos procesados:  
- Fuente (`encuestas_YYYYMM.xlsx`)  
- Periodo cubierto (mínimo y máximo de fechas)  
- Mecanismo de trazabilidad (`_ingest_ts`, `_source_file`, `_batch_id`)  

### 📊 **2. KPIs**
Resumen con las métricas más importantes (totales, medias y porcentajes).

### 📈 **3. Tablas de Resultados**
Incluye:
- **Distribución de satisfacción** (de 1 a 10 + NS/NC)  
- **Evolución mensual** de la media de satisfacción y número de encuestas  

Ejemplo:
```text
## Distribución de satisfacción (1–10 + NS/NC)
| satisf_str | n |
|-------------|---|
| 1 | 167 |
| 2 | 171 |
| 3 | 180 |
| ... | ... |
| 10 | 149 |
| NS/NC | 227 |
