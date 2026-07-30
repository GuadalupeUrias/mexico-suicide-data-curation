# Metodología

> Estado: completo — pipeline validado sobre 2023 (piloto) y consolidado
> 2019-2024 (49,918 registros).

## 1. Fuente y alcance
- Fuente: INEGI, Estadísticas de Defunciones Registradas (EDR), 2006-2023.
- Filtro de inclusión: `tipo_defun` = accidental/violenta AND presunción = suicidio
  (CIE-10 X60-X84).
- Nivel de agregación: registro individual (microdato).

## 2. Reglas de filtrado
| Regla | Justificación |
|---|---|
| `Tipo_defun == 3` | INEGI codifica la presunción de tipo de defunción en esta variable; `3` = "Suicidio (Lesión autoinfligida)". Es el filtro central del universo de estudio. |
| Verificación cruzada con `Causa_def` (CIE-10 X60-X84) | Validación secundaria: las causas CIE-10 de lesión autoinfligida deben ser consistentes con `Tipo_defun == 3`. Discrepancias se documentan como hallazgo de calidad. |
| Verificación de magnitud contra cifra publicada | INEGI reportó ~9,085 casos de suicidio en 2023 (10.8% de 84,118 defunciones por causas externas, Nota Técnica EDR 2023). El conteo del filtro propio debe aproximarse a esta cifra; diferencias se explican y documentan. |

## 3. Reglas de limpieza
| Campo | Problema detectado | Regla aplicada | Justificación |
|---|---|---|---|
| Múltiples (ver `DEFUN_NULL_LIKE_CODES` en `cleaning_utils.py`) | Códigos categóricos (8, 9, 88, 99, 997, 998, 999...) representan "no especificado"/"se ignora", pero pandas no los detecta como NaN | Recodificación explícita a `NaN` con `recode_null_codes()` | No se imputa: se prioriza la honestidad del dato sobre la completitud aparente (principio FAIR) |
| `Edad` | Mezcla unidad (horas/días/meses/años) y valor en un solo código numérico | Separación en `edad_valor` + `edad_unidad` con `split_edad()`, conservando `Edad` original | Un campo mixto no es analizable directamente; se preserva trazabilidad no destruyendo el original |
| `Causa_def`, `Ent_ocurr`, `Sexo` | Códigos sin etiqueta legible | Traducción vía `translate_catalog()` cruzando contra catálogos oficiales (`CATMINDE.dbf`, `CATEMLDE23.dbf`), agregando columnas `*_desc` sin eliminar el código original | Mantener ambas versiones permite trazabilidad y facilita el análisis exploratorio |

## 4. Normalización de catálogos
- **Códigos de entidad/municipio**: catálogo INEGI vigente usado como referencia =
  `CATEMLDE23.dbf` (Catálogo Único de Claves de Áreas Geoestadísticas Estatales,
  Municipales y Localidades). Validado sin códigos huérfanos contra el dataset 2023
  (ver `quality_report.md`, sección de validaciones).
- **Nombres de columna**: los archivos `.dbf` de origen guardan los campos en
  MAYÚSCULAS; se normalizan al formato documentado (`Ent_ocurr`, no `ENT_OCURR`)
  con `normalize_columns()`, usando como referencia canónica el diseño de registro
  oficial de INEGI: https://www.inegi.org.mx/rnm/index.php/catalog/1140 (tabla
  DEFUN24, Estadísticas de Defunciones Registradas 2024, 74 variables).
- **Cambios de nomenclatura detectados entre años**: ver sección 7b (`PRESUNTO` →
  `Tipo_defun`).
- **Corrección de documentación (hallazgo del control de calidad interno)**:
  al cruzar las descripciones cortas usadas en versiones tempranas de este
  documento contra el diseño de registro oficial, se detectó que `Lugar_ocur`
  y `Sitio_ocur` estaban descritas de forma invertida. La corrección:
  - `Lugar_ocur` = tipo de **sitio físico** donde ocurrió la lesión (vivienda,
    calle, escuela, área industrial, etc. — pregunta 32 del certificado).
  - `Sitio_ocur` = tipo de **institución de salud** donde ocurrió la defunción
    (IMSS, ISSSTE, vía pública, hogar, etc. — pregunta 19 del certificado).
  Este hallazgo se documenta como evidencia del propio proceso de control de
  calidad: las descripciones actuales en `data_dictionary.md` (generado por
  `generar_data_dictionary()` en `cleaning_utils.py`) ya reflejan la versión
  corregida, tomada directamente del documento oficial de INEGI, no de
  inferencia por nomenclatura.

## 5. Manejo de valores nulos / no especificados
- **Principio general**: no se imputa ningún valor faltante o "no especificado".
  Se preservan como `NaN` explícito (ver sección 3, regla de recodificación) para
  mantener la honestidad del dato sobre la completitud aparente (principio FAIR:
  Reusable).
- **Umbral de precaución**: variables con más de 15% de valores "no especificado"
  se marcan explícitamente en `quality_report.md` como de uso cauteloso en análisis
  que dependan de ellas (ej. `Ocurr_trab`, `Derechohab`, `Asist_medi`). El detalle
  completo por variable está en `quality_report.md`, sección "Nulos ocultos".
- **Caso especial multi-año**: variables ausentes del certificado en 2019-2021
  (ej. `Afromex`, `Cirugia`, `Encefalica`) se dejan como `NaN` para esos años al
  consolidar, no se excluyen esos años ni se imputa un valor por defecto (ver
  sección 7b). Esto se refleja directamente en `data_dictionary.md`: esas
  variables muestran ~47% de nulos en el consolidado, proporcional a los 3 de 6
  años donde no existían — es una verificación cruzada interna de que la regla
  se aplicó correctamente.

## 6. Deduplicación
- Se verificó con `duplicate_report()` sobre registros exactos (todas las columnas).
- **Resultado 2023 (piloto)**: 0 duplicados sobre 9,072 registros.
- **Resultado consolidado 2019-2024**: 0 duplicados sobre 49,918 registros.
- No se aplicó ninguna regla de deduplicación porque no se encontraron casos.
  Se documenta el resultado (no solo la ausencia de regla) porque un reporte de
  calidad debe mostrar que se buscó, no asumir que no había que buscar.

## 7. Saltos metodológicos conocidos (documentados por INEGI)
- Hasta 2005: datos captados en agencias del Ministerio Público.
- Desde 2006: datos derivados de estadísticas de mortalidad (EDR).
- **Hallazgo real (piloto multi-año 2019-2024):** se documentó como hipótesis
  pendiente un posible efecto de subregistro/caída en 2020-2021 por la
  pandemia. La evidencia real **no confirma esa hipótesis** — el conteo de
  suicidio muestra incremento sostenido en esos años (2019: 7,225 → 2020:
  7,896 [+9.29%] → 2021: 8,433 [+6.80%]), sin caída. La tendencia general
  2019-2023 es un aumento del 25.6% en 5 años, con aparente estabilización
  entre 2023 (9,072) y 2024 preliminar (9,051, -0.23%). Se documenta el
  hallazgo real en lugar de la hipótesis original, y se marca 2024 como
  preliminar (ver 7b) al interpretar la aparente estabilización.

## 7b. Diferencias de esquema detectadas al escalar a multi-año (piloto 2019-2023)
- **`PRESUNTO` (2019-2021) es la misma variable que `Tipo_defun` (2022-2023)** —
  cambio de nombre entre versiones del certificado de defunción, no una
  variable nueva. Confirmado por evidencia cruzada: el código `3` (Suicidio)
  en `PRESUNTO` para 2019 arrojó 7,225 casos, contra 7,233 publicados
  oficialmente por INEGI (diferencia 0.11%) — el mismo margen visto en la
  validación de 2023 (0.14%). Se maneja con un alias automático
  (`COLUMN_ALIASES` en `cleaning_utils.py`) que renombra `PRESUNTO` a
  `Tipo_defun` antes de filtrar.
- Variables ausentes en 2019-2021 pero presentes en 2022-2023: `Afromex`,
  `Conindig`, `Cirugia`, `Cod_adicio`, `Cve_lengua`, `Donador`, `Encefalica`,
  `Ent_nac`, `Gramos`, `Loc_regis`, `Nacesp_cve`, `Natviole`, `Sem_gest`,
  `Tloc_regis`, `Usonecrops`. Estas son adiciones reales al certificado de
  defunción a través del tiempo (ej. `Afromex`/`Conindig` se basan en el
  Censo de Población y Vivienda 2020, consistente con no existir antes).
  Se dejan como `NaN` para los años donde no existan al consolidar — no se
  imputan ni se excluyen esos años.
- 2022 solo tiene 1 variable ausente (`Vio_fami`) respecto al esquema de
  2023 — diferencia menor, mismo tratamiento (NaN).
- **2024 son cifras PRELIMINARES** según el boletín oficial de INEGI (EDR
  2024, publicado 2025) — sujetas a ajuste cuando se publique la versión
  definitiva. Se documenta esta condición en `quality_report.md` al reportar
  resultados de ese año; cualquier comparación contra cifras oficiales para
  2024 debe considerarse provisional.

## 8. Principios FAIR aplicados
- **Findable**: metadatos claros en este documento + data dictionary; repositorio
  registrado como obra citable en Zenodo, DOI: `10.5281/zenodo.21686584`.
- **Accessible**: datos procesados en formato abierto (CSV) en `data/processed/`.
- **Interoperable**: nomenclatura de columnas estandarizada, tipos de dato
  explícitos, códigos de catálogo documentados con su significado oficial.
- **Reusable**: licencia MIT (código), metodología documentada, código
  reproducible, diccionario de datos generado automáticamente a partir de la
  fuente oficial (ver sección 9).

## 9. Diccionario de datos automatizado
- `docs/data_dictionary.md` se genera con `generar_data_dictionary()` en
  `src/cleaning_utils.py`, ejecutado desde `notebooks/05_documentation.ipynb`.
- Las descripciones de cada variable (`DEFUN_DESCRIPTIONS` en `cleaning_utils.py`)
  provienen del diseño de registro oficial de INEGI, no de inferencia por
  nomenclatura — esto evita el tipo de error corregido en la sección 4
  (`Lugar_ocur`/`Sitio_ocur`).
- La función reporta cuántas variables quedan sin descripción (`TODO`) si se
  agrega una columna nueva al dataset que no esté en `DEFUN_DESCRIPTIONS`,
  para que nunca quede una variable sin documentar silenciosamente.
- Al reejecutarse (ej. si se agregan más años), el diccionario se actualiza
  solo — no requiere edición manual.
