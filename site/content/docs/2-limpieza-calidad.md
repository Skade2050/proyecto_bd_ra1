---
title: "2. Limpieza y Control de Calidad"
description: "Normalización, depuración y aplicación de reglas de calidad para generar datos limpios y en cuarentena."
---
## Contexto de la Fase  

Una vez que los datos de encuestas han sido **ingeridos y almacenados** correctamente, el siguiente paso del pipeline consiste en **limpiar y validar** la información.  

El objetivo de esta fase es asegurar que los registros sean **coherentes, completos y útiles** para los análisis posteriores.  
Esto implica detectar errores comunes (fechas inválidas, puntuaciones fuera de rango, identificadores vacíos, etc.) y aislar esos casos en una **zona de cuarentena** para no alterar los resultados finales.  

---

## 1. Proceso de Limpieza  

La limpieza se realiza mediante la función `clean_data()` ubicada en el archivo `clean.py`.  
Este proceso trabaja sobre los datos almacenados en la tabla `raw_encuestas` y genera dos salidas principales:

- **`clean`** → datos válidos y listos para el análisis.  
- **`quarantine`** → registros con errores o inconsistencias.

### Pasos principales:

1. ### **Normalización de Nombres y Textos**  
   - Convierte todos los nombres de columnas a minúsculas.  
   - Elimina espacios innecesarios en los textos.  
   - Homogeneiza los valores para evitar duplicidades por diferencias de formato (por ejemplo, " Online" y "online" se tratan igual).

2. ### **Conversión de Tipos de Datos**  
   - La columna `fecha` se transforma en formato **fecha estándar (`datetime`)**.  
   - La columna `satisfaccion` se convierte en valor **numérico (1 a 10)**.  
   - Valores como `"no sabe/no contesta"` o `"ns/nc"` se transforman en `NaN` (vacíos), para poder calcular correctamente los promedios.  

3. ### **Detección de Duplicados**  
   - Si una misma respuesta (`id_respuesta`) aparece varias veces, se conserva **solo la más reciente**, siguiendo la política *“último gana”*.  
   - Esta decisión se basa en el campo `_ingest_ts` (marca temporal del momento en que se cargó el dato).

4. ### **Validación de Calidad**  
   Se aplican reglas automáticas para detectar registros inválidos:
   - `fecha_invalida`: cuando la fecha está vacía o no puede convertirse.  
   - `satisf_fuera_rango`: cuando la satisfacción no está entre 1 y 10.  
   - `id_respuesta_vacio`: cuando el identificador está en blanco o ausente.  

   Los registros que incumplen alguna de estas reglas se envían a la **cuarentena** con una explicación de la causa.

---

## 2. Estructura del Resultado  

Al finalizar el proceso, el pipeline devuelve dos conjuntos de datos:

| Salida | Descripción | Ejemplo de uso |
|:--------|:-------------|:----------------|
| `clean` | Encuestas limpias y válidas | Usadas para calcular medias, distribuciones, KPIs, etc. |
| `quarantine` | Respuestas con errores o valores no válidos | Guardadas para revisión manual o trazabilidad. |

En la tabla `quarantine`, los motivos se guardan en la columna `_quarantine_reason`, por ejemplo:  
```text
fecha_invalida
satisf_fuera_rango
fecha_invalida;satisf_fuera_rango
