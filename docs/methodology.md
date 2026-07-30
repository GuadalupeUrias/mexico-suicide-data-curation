# Metodología

> Estado: borrador — se completa durante el perfilado y limpieza.

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
- Códigos de entidad/municipio: catálogo INEGI vigente usado como referencia = _pendiente_.
- Cambios de nomenclatura detectados entre años: _pendiente_.

## 5. Manejo de valores nulos / no especificados
_pendiente_

## 6. Deduplicación
_pendiente_

## 7. Saltos metodológicos conocidos (documentados por INEGI)
- Hasta 2005: datos captados en agencias del Ministerio Público.
- Desde 2006: datos derivados de estadísticas de mortalidad (EDR).
- 2020-2021: posible efecto de subregistro/retraso por pandemia — verificar en perfilado.

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

## 8. Principios FAIR aplicados
- **Findable**: metadatos claros en este documento + data dictionary.
- **Accessible**: datos procesados en formato abierto (CSV) en `data/processed/`.
- **Interoperable**: nomenclatura de columnas estandarizada, tipos de dato explícitos.
- **Reusable**: licencia clara, metodología documentada, código reproducible.
