#!/usr/bin/env bash
# Configura el entorno del proyecto de un solo paso.
# Uso: bash setup.sh

set -e

echo "==> Creando entorno virtual (venv)..."
python3 -m venv venv

echo "==> Activando entorno virtual..."
source venv/bin/activate

echo "==> Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Registrando kernel de Jupyter para este proyecto..."
python -m ipykernel install --user --name=mexico-suicide-data-curation --display-name "Python (mexico-suicide-data-curation)"

echo ""
echo "Listo. Pasos siguientes:"
echo "1. Abre el proyecto en VS Code: code ."
echo "2. Cuando aparezca el aviso de extensiones recomendadas, dale 'Install All'."
echo "3. Abre cualquier notebook en notebooks/ y selecciona el kernel 'Python (mexico-suicide-data-curation)'."
