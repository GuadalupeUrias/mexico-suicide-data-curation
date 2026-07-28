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
| _pendiente_ | _pendiente_ |

## 3. Reglas de limpieza
| Campo | Problema detectado | Regla aplicada | Justificación |
|---|---|---|---|
| _pendiente (se llena en 02_cleaning)_ | | | |

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

## 8. Principios FAIR aplicados
- **Findable**: metadatos claros en este documento + data dictionary.
- **Accessible**: datos procesados en formato abierto (CSV) en `data/processed/`.
- **Interoperable**: nomenclatura de columnas estandarizada, tipos de dato explícitos.
- **Reusable**: licencia clara, metodología documentada, código reproducible.
