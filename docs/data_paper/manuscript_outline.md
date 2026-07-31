# Esqueleto del data paper — Microdatos de suicidio en México (2019-2024)

Estado: borrador de estructura. Completar secciones marcadas `[PENDIENTE]`.
No reemplaza methodology.md/quality_report.md/data_dictionary.md — este
documento traduce esos archivos a formato de articulo de datos. Ellos
siguen siendo la fuente de verdad metodologica del pipeline.

---

## Titulo de trabajo

"Curaduria y documentacion FAIR de microdatos de mortalidad por suicidio
en Mexico (2019-2024): un conjunto de datos reproducible"

`[PENDIENTE: version en ingles para revista internacional -- "Curation
and FAIR Documentation of Suicide Mortality Microdata in Mexico
(2019-2024): A Reproducible Dataset"]`

## Palabras clave (5-6)

Suicidio; mortalidad; microdatos; ciencia abierta; FAIR; Mexico

## Tipo de contribucion

Data paper / data descriptor (no articulo de resultados). El objetivo es
documentar la calidad y reproducibilidad de un conjunto de datos para su
reutilizacion, no probar una hipotesis. Revistas objetivo tipicas: *Data
in Brief*, *Scientific Data*, o secciones de "nota de datos" en revistas
regionales latinoamericanas.

`[PENDIENTE: decidir revista objetivo -- afecta formato exacto de
secciones, limite de palabras, y si se requiere manuscrito companero
("research article" que use el dataset) segun politica de la revista]`

---

## Abstract (150-250 palabras, formato tipico de data descriptor)

- **Contexto (1-2 lineas):** el suicidio es un problema de salud publica
  en Mexico; INEGI publica microdatos oficiales pero sin curaduria
  orientada a reutilizacion por terceros.
- **Que se hizo (2-3 lineas):** se curo, valido y documento un
  subconjunto de microdatos de defunciones por suicidio (2019-2024),
  aplicando principios FAIR: filtrado por `Tipo_defun == 3`, preservacion
  explicita de nulos (sin imputar), correccion documentada de errores de
  descripcion de variables, y trazabilidad completa de decisiones.
- **Que contiene el dataset (2-3 lineas):** 49,918 registros nacionales,
  6 anios (2019-2024), variables de residencia/ocurrencia, lugar y sitio
  de ocurrencia, catalogo de descripciones oficiales de variables
  (`DEFUN_DESCRIPTIONS`).
- **Validacion (1-2 lineas):** 6/6 verificaciones de calidad superadas
  (duplicados, codigos geograficos huerfanos, consistencia entre anios,
  validacion cruzada contra cifras oficiales INEGI con diferencia entre
  0.00% y 0.98% en anios con cifra definitiva).
- **Disponibilidad (1 linea):** repositorio en GitHub, DOI en Zenodo
  (`10.5281/zenodo.21686584`), licencia MIT para el codigo.

---

## 1. Contexto y motivacion

- El suicidio como problema de salud publica en Mexico (cifras generales,
  fuente INEGI/OMS).
- INEGI capta suicidios dentro de las Estadisticas de Defunciones
  Registradas (EDR) desde 2006, con 74 variables por registro.
- Brecha: los microdatos oficiales estan disponibles, pero sin curaduria
  documentada orientada a reutilizacion (sin diccionario de datos
  enriquecido, sin reporte de calidad publico, sin trazabilidad de
  decisiones de limpieza).
- Objetivo del data paper: documentar formalmente el proceso de curaduria
  para que el dataset resultante sea reutilizable por otros
  investigadores sin repetir el trabajo de limpieza desde cero.

`[RESUELTO: ver docs/data_paper/references.md -- Campuzano Rincon et al.
(2022), Martinez Salgado (2010) e INEGI (2025) cubren esta seccion]`

## 2. Metodos de construccion del dataset

Tomado directamente de `methodology.md` -- resumir, no reescribir desde
cero:

- Fuente: microdatos EDR-INEGI, formato `.dbf`, 74 variables, 2019-2024.
- Filtro de caso: `Tipo_defun == 3`; alias `PRESUNTO` (2019-2021) =
  `Tipo_defun` (2022+).
- Principio de no imputacion: nulos preservados como `NaN` explicito.
- Correccion documentada de error de documentacion: `Lugar_ocur`
  (tipo de sitio fisico) vs. `Sitio_ocur` (tipo de institucion de salud)
  estaban invertidos en una version previa -- corregido y dejado como
  evidencia de control de calidad del pipeline.
- Fuente de descripciones oficiales de variables: diseno de registro
  INEGI (`https://www.inegi.org.mx/rnm/index.php/catalog/1140`).
- Pipeline reproducible: `01_profiling` -> `02_cleaning` ->
  `03_validation` -> `04_multi_year_pilot` -> `05_documentation`.

## 3. Descripcion del dataset

- Estructura de carpetas del repositorio (`data/raw`, `data/interim`,
  `data/processed`).
- Resumen del diccionario de datos (`data_dictionary.md`): numero de
  variables documentadas, categorias (identificacion, geografia,
  demograficas, caracteristicas de la defuncion).
- Formato de archivos, encoding, convenciones de nombres.
- Cobertura temporal y geografica (nacional, 2019-2024).

**Tabla de cobertura temporal (confirmado con datos reales):**

| Año | N registros |
|---|---|
| 2019 | 7,225 |
| 2020 | 7,896 |
| 2021 | 8,433 |
| 2022 | 8,241 |
| 2023 | 9,072 |
| 2024 | 9,051 |
| **Total 2019-2024** | **49,918** |

Crecimiento 2019→2024: +25.3%, consistente con el hallazgo ya
documentado de +25.6% acumulado en el periodo (pequeña diferencia
probablemente por redondeo o por cifras preliminares vs. definitivas de
2024). Sirve como verificacion cruzada de que el consolidado no se
corrompio ni cambio entre sesiones de trabajo.

`[RESUELTO]`

## 4. Validacion tecnica

**Checklist de validación (6/6, `quality_report.md`):**

1. Volumen del filtro `Tipo_defun == 3` validado contra cifras oficiales
   INEGI. Diferencia entre 0.00% y 0.98% en años con cifra definitiva
   publicada (2019: 0.11%, 2020: 0.00%, 2021: 0.98%); diferencias mayores
   en 2022 y 2024 corresponden a comparaciones contra cifras que INEGI
   mismo etiqueta como preliminares, no a error del pipeline.
2. Duplicados exactos: 0 en cada uno de los 6 años (49,918 registros
   totales).
3. Nulos explícitos (NaN) revisados por columna: 1 columna con 100% nulo
   (`Razon_m`, estructural — variable exclusiva de defunciones maternas,
   no aplica a suicidios); el resto de las 73 columnas sin NaN explícito.
4. Nulos ocultos (códigos categóricos "no especificado"/"se ignora")
   revisados por columna: variables demográficas centrales (sexo, edad,
   entidad) casi completas (sexo no especificado: 0.02%); variables de
   *contexto del hecho* (si ocurrió en el trabajo, atención médica
   previa, afiliación a salud, lugar del hecho) entre 15% y 26% no
   especificado — documentado explícitamente, no imputado (principio
   FAIR de preservar honestidad del dato).
5. Rangos de fecha válidos: 0.24%-0.57% de fechas inválidas por año, sin
   tendencia atípica.
6. Códigos de entidad/municipio contra catálogo vigente INEGI: 0 códigos
   huérfanos en los 6 años (2019-2024), validado individualmente por
   año.

**Consistencia entre años:** auditada con `audit_multiple_years()` antes
de consolidar; alias `PRESUNTO` → `Tipo_defun` (2019-2021 usan el nombre
antiguo de la variable) aplicado y validado.

**Limitación documentada explícitamente (no oculta):** las variables de
contexto del hecho (Ocurr_trab, Derechohab, Asist_medi, Lugar_ocur,
Ocupacion) tienen 15-26% de "no especificado" — se recomienda su uso con
precaución en análisis que dependan de ellas. No se imputan.

`[RESUELTO]`

## 5. Trabajos relacionados

Verificado contra las fuentes originales (no citar de memoria):

- **Palacio-Mejía, L. S., Hernández-Ávila, J. E., Morales-Carmona, E.,
  Espín-Arellano, L. I., & Molina-Vélez, D. (2022).** Defunciones
  registradas INEGI 1990-2024. Base de datos estandarizada [Dataset].
  Unidad de Inteligencia en Salud Pública, Instituto Nacional de Salud
  Pública. https://riisp.insp.mx/nada/index.php/catalog/21
  Compilacion, estandarizacion e integracion via ETL de todas las causas
  de muerte, con revision de consistencia entre anios (dimensiones de
  exactitud, consistencia, cobertura, puntualidad, integridad y
  trazabilidad). Diferencia con el presente dataset: cobertura de
  *todas* las causas (el suicidio es una fila mas dentro del agregado),
  sin documentacion granular de decisiones de limpieza ni reporte de
  calidad publico independiente por causa especifica.

- **Morin-Garcia, J. C., Lopez-Arevalo, I., & Gonzalez-Compean, J. L.
  (2025).** Mortality Rates in Mexico (2000-2024): Death Counts - Crude
  and Age-Standardized Mortality Rates (Version 1) [Dataset]. Zenodo.
  https://doi.org/10.5281/zenodo.17739712
  Dataset curado por investigadores del CINVESTAV, con conteos y tasas
  (cruda y estandarizada por edad, Metodo Directo) por codigo CIE-10,
  grupo de edad, sexo y nivel geografico (nacional/estatal/municipal),
  organizado en archivos por capitulo de causa. Diferencia: mortalidad
  general agregada en tasas por causa/region, no microdatos a nivel de
  registro individual curados con trazabilidad de decisiones; el
  suicidio aparaceria como una fila mas dentro del capitulo de causas
  externas, sin el nivel de documentacion FAIR que aqui se ofrece.

- **Posicionamiento del presente dataset:** primer conjunto de datos
  *especifico de suicidio* (no mortalidad general) con documentacion FAIR
  granular (diccionario enriquecido, reporte de calidad antes/despues,
  decisiones de limpieza trazadas y errores de documentacion corregidos
  de forma explicita) y pipeline reproducible con DOI propio.

`[RESUELTO: autoria formal confirmada via ficha de citacion oficial del
INSP -- ver references.md, nota de verificacion, para el pendiente
restante sobre catalog/11 vs. catalog/21]`

## 6. Valor de reutilizacion

- Para quien es util: investigadores en salud publica, epidemiologia,
  ciencias sociales que estudien suicidio en Mexico sin partir de datos
  crudos.
- Casos de uso ya demostrados por el propio equipo: sirvio como base para
  el analisis espacial de Chihuahua (repo separado
  `chihuahua-suicide-spatial-analysis`), evidencia de que el dataset
  soporta analisis subnacionales sin retrabajo.
- Extensiones posibles: analisis por edad/sexo, comparaciones
  interestatales, series de tiempo con covariables ambientales.

## 7. Disponibilidad de datos y codigo

- Repositorio: GitHub (`urcamagu-coder`).
- DOI: Zenodo `10.5281/zenodo.21686584`.
- Licencia: MIT (codigo).
- ORCID: `https://orcid.org/0009-0008-0081-4676`.

---

## Nota final del esqueleto

Secciones 1, 3, 4 y 5 resueltas con datos verificados. Pendiente real:

- Sección 2 y 6: transcripcion/redaccion corta desde `methodology.md`
  (2) y valor de reutilizacion propio (6) -- no requieren investigacion
  nueva.
- Sección 7: confirmar que los datos de disponibilidad (GitHub, DOI,
  licencia, ORCID) siguen vigentes tal cual estan.
- Revista objetivo: decision pendiente, afecta formato final.
- `catalog/11` vs. `catalog/21` (ver nota en `references.md`): pendiente
  de verificar antes de la version final del manuscrito.
