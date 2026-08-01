# Reporte de calidad de datos

## Resumen ejecutivo — Consolidado multi-año 2019-2024

| Métrica | Valor |
|---|---|
| Años consolidados | 2019, 2020, 2021, 2022, 2023, 2024 (2024 = cifras preliminares) |
| Registros totales (suicidio, `Tipo_defun`/`PRESUNTO == 3`) | 49,918 |
| Duplicados exactos | 0 (0.0%) en cada año individual |
| Consistencia de esquema | Auditada con `audit_multiple_years()`; alias `PRESUNTO`→`Tipo_defun`
  aplicado para 2019-2021 (ver `methodology.md`, sección 7b) |

### Perfilado por año (registros, duplicados, fechas inválidas)

| Año | Registros | Duplicados | Fechas inválidas | % fechas inválidas |
|---|---|---|---|---|
| 2019 | 7,225 | 0 | 30 | 0.42% |
| 2020 | 7,896 | 0 | 45 | 0.57% |
| 2021 | 8,433 | 0 | 30 | 0.36% |
| 2022 | 8,241 | 0 | 34 | 0.41% |
| 2023 | 9,072 | 0 | 33 | 0.36% |
| 2024 | 9,051 | 0 | 22 | 0.24% |

Nota: 0% de códigos "no especificado" (99/999) en entidad, municipio y causa de
ocurrencia en los 6 años — a diferencia de otras variables de contexto (ver tabla
de nulos ocultos más abajo), el lugar de ocurrencia casi siempre se registra en
el subconjunto de suicidios.

### Validación cruzada contra cifras oficiales INEGI (multi-año)

| Año | Conteo (pipeline) | Oficial preliminar | Oficial definitiva | Diferencia |
|---|---|---|---|---|
| 2019 | 7,225 | — | 7,233 | 0.11% |
| 2020 | 7,896 | 7,818 | **7,896** | **0.00%** |
| 2021 | 8,433 | — | 8,351 | 0.98% |
| 2022 | 8,241 | 8,123 | *(sin definitiva publicada aún)* | 1.45% vs. preliminar |
| 2023 | 9,072 | ~9,085 | — | 0.14% |
| 2024 | 9,051 | 8,856 (boletín Día Mundial) | 9,051 (comunicado EDR) | 0.00% vs. EDR |

**Lectura:** cuando existe cifra definitiva (2019, 2020, 2021), la diferencia
del pipeline queda entre 0.00% y 0.98%. Las diferencias mayores (2022, y el
8,856 de 2024) corresponden a comparaciones contra cifras que el propio INEGI
etiqueta como preliminares o pendientes de confronta con Secretaría de Salud —
no son errores del pipeline. Fuentes: comunicados de prensa anuales de INEGI
(EAP_Suicidio, EDR), citados en detalle en `methodology.md`.

## Resumen ejecutivo — Año piloto 2023 (DEFUN23.dbf)

| Métrica | Valor |
|---|---|
| Registros totales EDR 2023 (todas las causas) | ver `df_raw.shape` en `01_profiling.ipynb` |
| Registros de suicidio filtrados (`Tipo_defun == 3`) | 9,072 |
| Cifra oficial INEGI (Nota Técnica EDR 2023) | ~9,085 (10.8% de 84,118 causas externas) |
| Diferencia vs. cifra oficial | 13 casos (0.14%) — dentro de margen aceptable |
| Duplicados exactos | 0 (0.0%) |
| Columnas con 100% nulo (NaN explícito) | 2 (`Razon_m`, `Maternas` — ambas estructurales, exclusivas de defunciones maternas) |
| Columnas con >15% de "no especificado" oculto | 4 |

**Validación de filtro:** el conteo propio (9,072) se aproxima a la cifra publicada por
INEGI (~9,085) con una diferencia de 0.14%, atribuible a naturaleza preliminar/definitiva
de las cifras. Se considera el filtro `Tipo_defun == 3` **validado**.

## Nulos explícitos (detectados por pandas como NaN)

| Columna | % nulo | Explicación |
|---|---|---|
| Razon_m | 100.0% | Estructural: variable exclusiva de defunciones maternas, no aplica a suicidios |
| Maternas | 100.0% | Estructural: causas maternas detalladas (CIE-10), variable derivada exclusiva de defunciones maternas, no aplica a suicidios |
| Resto (72 columnas) | 0.0% | Sin NaN explícito |

## Nulos ocultos (códigos categóricos "no especificado"/"se ignora")

Detectados con `special_code_report()` — no son NaN para pandas, pero funcionalmente
representan información faltante. Variables con mayor incidencia (año piloto 2023,
n=9,072):

| Variable | Código | Significado del código | Conteo | % del total |
|---|---|---|---|---|
| Ocurr_trab | 9 | Se ignora si ocurrió en el trabajo | 2,330 | 25.68% |
| Derechohab | 99 | Afiliación a salud no especificada | 2,312 | 25.49% |
| Asist_medi | 9 | Se ignora si hubo atención médica | 1,701 | 18.75% |
| Ocupacion | 998 | Ocupación no especificada | 1,539 | 16.96% |
| Lugar_ocur | 9 | Se ignora el lugar del hecho | 1,353 | 14.91% |
| Conindig | 9 | No especificado (autoadscripción indígena) | 907 | 10.00% |
| Lengua | 9 | Se ignora si habla lengua indígena | 712 | 7.85% |
| Usonecrops | 8 | No aplica (uso de necropsia) | 691 | 7.62% |
| Afromex | 9 | No especificado (autoadscripción afromexicana) | 684 | 7.54% |
| Sitio_ocur | 99 | No especificado | 671 | 7.40% |
| Ocupacion | 999 | No aplica | 582 | 6.42% |
| Cond_act | 9 | Se ignora condición de actividad económica | 582 | 6.42% |
| Edo_civil | 9 | No especificado | 580 | 6.39% |
| Necropsia | 9 | No especificada | 435 | 4.79% |
| Escolarida | 99 | No especificada | 388 | 4.28% |
| Nacionalid | 9 | No especificada | 385 | 4.24% |
| Ent_nac | 998/999 | No especificado | 380 | 4.19% (combinado) |
| Area_ur | 9 | No especificada | 203 | 2.24% |
| Edad_agru | 30 | No especificada | 93 | 1.03% |
| Cond_cert | 8/9 | No especificado | 188 | 2.07% (combinado) |
| **Sexo** | 9 | **No especificado** | **2** | **0.02%** |

Nota: las 4 columnas que superan el umbral de 15% en este corte (2023) son
Ocurr_trab, Derechohab, Asist_medi y Ocupacion. `Lugar_ocur` (14.91%) queda
justo debajo del umbral y no debe incluirse en esa categoría.

**Referencia cruzada con el consolidado 2019-2024** (`data_dictionary.md`,
generado sobre las 49,918 filas): en el consolidado, las variables que
superan 15% de nulos son Ocurr_trab (26.71%), Derechohab (26.8%) y
Asist_medi (17.73%). `Lugar_ocur` baja a 10.66% y `Ocupacion` a 11.81% en el
consolidado — ambas por debajo del umbral. Al citar este umbral en el data
paper o en publicaciones derivadas, usar las cifras del consolidado
(`data_dictionary.md`), no las del piloto 2023, ya que el dataset descrito
es el multi-año completo.

**Lectura:** las variables demográficas centrales (Sexo, Edad, entidad) están casi
completas y son confiables para análisis. Las variables de **contexto del hecho**
con mayor incidencia de no especificado (ocurrencia en el trabajo, atención médica
previa, afiliación a salud) tienen entre 17.73% y 26.8% de información no
especificada en el consolidado — consistente con la naturaleza del proceso de
captación (Ministerio Público/Servicio Médico Forense no siempre reconstruye el
contexto completo en muertes violentas).

## Duplicados
- 0 registros duplicados exactos sobre 9,072 filas (piloto 2023). No requiere deduplicación.

## Limitaciones conocidas
- Subregistro y datos preliminares vs. definitivos (metodología INEGI, ver `methodology.md`).
- Variables de contexto del hecho con mayor incidencia de "no especificado" en el
  consolidado 2019-2024 (Ocurr_trab: 26.71%, Derechohab: 26.8%, Asist_medi: 17.73%)
  — se recomienda uso con precaución en análisis que dependan de ellas; no se
  imputan, se preservan como NaN explícito para mantener honestidad del dato
  (principio FAIR). Lugar_ocur (10.66%) y Ocupacion (11.81%) tienen nulos ocultos
  pero quedan por debajo del umbral de 15% en el consolidado.
- La variable Edad mezcla unidades (horas/días/meses/años) en un solo campo —
  requiere transformación antes de análisis de edad (ver `02_cleaning.ipynb`).
- Los campos del `.dbf` de origen están en MAYÚSCULAS; se normalizan al formato
  documentado con `normalize_columns()` al cargar.

## Diccionario de datos: verificación cruzada interna

`docs/data_dictionary.md` se genera automáticamente (`generar_data_dictionary()`
en `src/cleaning_utils.py`) a partir del consolidado multi-año. Los porcentajes
de nulos reportados ahí sirven como verificación cruzada de las reglas
documentadas en `methodology.md`:

- Variables ausentes en el certificado 2019-2021 (`Cirugia`, `Encefalica`,
  `Afromex`, etc.) muestran ~47.19% de nulos en el consolidado — consistente
  con que 3 de los 6 años (2019, 2020, 2021 = 23,554 de 49,918 registros,
  47.19%) no tenían esa variable. Esto confirma que la regla de "no imputar,
  dejar NaN cuando la variable no existía ese año" (sección 5 de
  `methodology.md`) se aplicó correctamente al consolidar.
- `Razon_m` y `Maternas` en 100% de nulos, consistente con lo ya documentado
  para 2023 (son estructurales: variables exclusivas de defunciones maternas).
- El umbral de "no especificado" >15% cambia según el corte de datos: en el
  piloto 2023 son 4 variables (Ocurr_trab, Derechohab, Asist_medi, Ocupacion);
  en el consolidado 2019-2024 son 3 (Ocurr_trab, Derechohab, Asist_medi) —
  `Ocupacion` baja de 16.96% a 11.81% al consolidar los 6 años. Esta diferencia
  es esperable (el piloto es una sola cohorte anual) y no indica un error, pero
  cualquier cifra citada en publicaciones debe especificar a qué corte
  corresponde.

## Validaciones aplicadas
- [x] Volumen del filtro validado contra cifra oficial INEGI — 2023: diferencia
  0.14%; multi-año 2019-2024: entre 0.00% y 0.98% contra cifras definitivas
  (ver tabla de validación cruzada arriba)
- [x] Duplicados exactos verificados — 0 encontrados en cada uno de los 6 años
- [x] Nulos explícitos (NaN) revisados por columna
- [x] Nulos ocultos (códigos categóricos) revisados por columna
- [x] Rangos de fecha válidos — validado en `03_validation.ipynb` (2023: 33
  inválidas, 0.36%) y confirmado por año en el perfilado multi-año (0.24%-0.57%,
  sin tendencia atípica por año)
- [x] Códigos de entidad/municipio contra catálogo vigente (`CATEMLDE23.dbf`) —
  validado para 2023 en `03_validation.ipynb`, 0 códigos huérfanos
- [x] Consistencia entre años — auditada con `audit_multiple_years()` antes de
  consolidar; alias `PRESUNTO`→`Tipo_defun` aplicado y validado (ver
  `methodology.md`, sección 7b)
- [x] Códigos de entidad/municipio contra catálogo vigente — validado para
  los 6 años individualmente (`04_multi_year_pilot.ipynb`, sección 5b), 0
  códigos huérfanos y 0 registros afectados en todos los años (2019-2024)

## Estado del checklist: completo (6/6)
