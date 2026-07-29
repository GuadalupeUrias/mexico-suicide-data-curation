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

El perfilado se realiza con pandas puro (sin `ydata-profiling`, no compatible aún
con Python 3.13+/3.14) mediante funciones propias en `src/cleaning_utils.py`.

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

### Opción rápida (recomendada)
```bash
# Mac/Linux
bash setup.sh

# Windows
setup.bat
```
Esto crea el entorno virtual, instala dependencias y registra el kernel de Jupyter.
En Windows, si no tienes Python instalado, el script lo instala automáticamente
con `winget` (viene incluido en Windows 10/11 actualizado). Si eso ocurre, cierra
y reabre la terminal una vez (limitación de Windows, no del script) y vuelve a
correr `setup.bat`.

### Opción manual
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m ipykernel install --user --name=mexico-suicide-data-curation --display-name "Python (mexico-suicide-data-curation)"
```

### En VS Code
1. Abre la carpeta del proyecto: `code .`
2. Acepta instalar las extensiones recomendadas cuando aparezca el aviso (o `Ctrl+Shift+P` → "Extensions: Show Recommended Extensions")
3. `Ctrl+Shift+P` → "Python: Select Interpreter" → elige `./venv`
4. Abre cualquier notebook en `notebooks/`, selecciona el kernel del proyecto, y corre celdas con `Shift+Enter`

Ejecutar los notebooks en orden: `01_profiling.ipynb` → `02_cleaning.ipynb` → `03_validation.ipynb`.

## Nota sobre el tema
Este proyecto usa datos públicos y agregados con fines metodológicos de curaduría
de datos (perfilado, limpieza, validación). No representa un análisis clínico ni
sustituye fuentes oficiales de salud pública.

## Licencia
Código bajo licencia MIT (ver [LICENSE](LICENSE)). Datos originales propiedad de INEGI.
