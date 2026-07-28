# Curaduría de datos: Estadísticas de suicidio en México (INEGI, 2006-2023)

## Objetivo
Curar, limpiar y validar los microdatos de suicidio de México, derivados de las
Estadísticas de Defunciones Registradas (EDR) del INEGI, aplicando principios FAIR
(Findable, Accessible, Interoperable, Reusable) y documentando cada decisión
metodológica.

## Fuente de datos
- INEGI. Estadísticas de Defunciones Registradas (EDR), microdatos 2006-2023.
- Filtrado por tipo de defunción (accidental/violenta) y presunción de intencionalidad
  (suicidio), CIE-10 X60-X84.
- Descarga: https://www.inegi.org.mx/app/descarga/
- Uso abierto bajo términos de INEGI. Los datos originales son propiedad de INEGI.

## Metodología
Ver [docs/methodology.md](docs/methodology.md) para el detalle completo de reglas
de filtrado, limpieza y normalización de catálogos.

## Diccionario de datos
Ver [docs/data_dictionary.md](docs/data_dictionary.md).

## Resultados
Ver [docs/quality_report.md](docs/quality_report.md) para métricas antes/después
(registros, % nulos, duplicados, inconsistencias resueltas).

## Estructura del repositorio
```
├── data/
│   ├── raw/          # datos originales sin modificar
│   ├── interim/       # pasos intermedios de limpieza
│   └── processed/     # dataset final limpio y validado
├── docs/
│   ├── data_dictionary.md
│   ├── methodology.md
│   └── quality_report.md
├── notebooks/
│   ├── 01_profiling.ipynb
│   ├── 02_cleaning.ipynb
│   └── 03_validation.ipynb
├── src/
│   └── cleaning_utils.py
└── requirements.txt
```

## Cómo reproducir
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```
Ejecutar en orden: `01_profiling.ipynb` → `02_cleaning.ipynb` → `03_validation.ipynb`.

## Nota sobre el tema
Este proyecto usa datos públicos y agregados con fines metodológicos de curaduría
de datos (perfilado, limpieza, validación). No representa un análisis clínico ni
sustituye fuentes oficiales de salud pública.

## Licencia
Código bajo licencia MIT (ver [LICENSE](LICENSE)). Datos originales propiedad de INEGI.
