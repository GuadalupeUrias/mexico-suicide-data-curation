# Curaduría de datos: Suicidio en México (INEGI, 2019-2024)

[![DOI](https://zenodo.org/badge/1315245532.svg)](https://zenodo.org/badge/latestdoi/1315245532)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Pipeline reproducible de perfilado, limpieza y validación de microdatos oficiales
de mortalidad por suicidio en México, aplicando principios **FAIR** (Findable,
Accessible, Interoperable, Reusable). Construido como pieza de portafolio para
servicios de curaduría de datos.

## Hallazgo principal

Entre 2019 y 2023, los suicidios registrados en México aumentaron **25.6%**
(7,225 → 9,072 casos). La hipótesis inicial de este proyecto era que 2020-2021
mostraría una caída o subregistro asociado a la pandemia — **la evidencia no
la confirma**: ambos años muestran incremento sostenido (+9.29% y +6.80%
respectivamente). Este hallazgo, corregido y documentado durante el propio
proceso de validación, es un ejemplo de por qué la trazabilidad metodológica
importa tanto como el resultado.

## Por qué este dataset

Chihuahua es la entidad federativa con la tasa de suicidio más alta de México
desde al menos 2022, casi triplicando la media nacional en 2024 (16.4 vs. 6.8
por cada 100 mil habitantes). Este repositorio es la base de curaduría para
análisis posteriores enfocados en esa entidad.

## Fuente de los datos

INEGI, Estadísticas de Defunciones Registradas (EDR), microdatos anuales
2019-2024 (2024 = cifras preliminares). Filtro de inclusión: `Tipo_defun == 3`
(lesión autoinfligida intencional), con alias documentado para el cambio de
nombre de variable (`PRESUNTO` en 2019-2021 → `Tipo_defun` desde 2022).

Catálogo de metadatos oficial: https://www.inegi.org.mx/rnm/index.php/catalog/1140

## Resultados de validación

| Métrica | Resultado |
|---|---|
| Registros consolidados | 49,918 (6 años) |
| Duplicados exactos | 0 en cada año |
| Códigos geográficos huérfanos | 0 en cada año |
| Diferencia vs. cifra oficial INEGI | 0.00%-0.98% (años con cifra definitiva) |
| Consistencia `Tipo_defun` vs. CIE-10 (X60-X84) | 100% |

Detalle completo en [`docs/quality_report.md`](docs/quality_report.md).

## Estructura del repositorio

```
data/
  raw/          Microdatos originales sin modificar (.dbf), por año
  interim/      Datos filtrados, sin limpiar (handoff entre notebooks)
  processed/    Dataset limpio y consolidado (.csv)
docs/
  methodology.md        Reglas de filtrado, limpieza y decisiones documentadas
  quality_report.md     Validación antes/después, cifras de calidad
  data_dictionary.md    Diccionario de datos (generado automáticamente)
  figuras/               Visualizaciones exploratorias
notebooks/
  01_profiling.ipynb          Perfilado inicial (año piloto 2023)
  02_cleaning.ipynb           Limpieza y visualizaciones (año piloto 2023)
  03_validation.ipynb         Validación de calidad (año piloto 2023)
  04_multi_year_pilot.ipynb   Escalamiento a 6 años (2019-2024)
  05_documentation.ipynb      Generación automatizada del diccionario de datos
src/
  cleaning_utils.py    Funciones reutilizables (carga, limpieza, validación)
```

## Cómo reproducir

```bash
pip install -r requirements.txt
```

Correr los notebooks en orden (01 → 05). Cada uno documenta su handoff de
entrada/salida en la primera celda markdown. Ver
[`docs/methodology.md`](docs/methodology.md) para las decisiones detrás de
cada regla de limpieza.

## Principios FAIR aplicados

- **Findable** — DOI vía Zenodo, metadatos documentados en este README y en
  `docs/`.
- **Accessible** — datos procesados en CSV, formato abierto, en `data/processed/`.
- **Interoperable** — nomenclatura de columnas estandarizada; códigos
  categóricos documentados con su significado oficial (no solo el número).
- **Reusable** — licencia MIT, metodología y decisiones trazables, código
  reproducible.

## Autoría

Proyecto desarrollado como parte de un portafolio de servicios de curaduría,
limpieza y validación de datos.

ORCID: https://orcid.org/0009-0008-0081-4676

## Licencia

Código bajo licencia MIT (ver [`LICENSE`](LICENSE)). Los datos originales
pertenecen a INEGI y se usan bajo su política de datos abiertos.
