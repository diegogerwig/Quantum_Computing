#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

echo "========================================"
echo "🚀 Initializing Qiskit Exam Simulator"
echo "========================================"

# 1. Comprobar si uv está instalado
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' is not installed. Please install it first (e.g., pip install uv)."
    exit 1
fi

# 2. Crear el entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment with uv..."
    uv venv
else
    echo "✅ Virtual environment already exists."
fi

# 3. Activar el entorno virtual
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# 4. Instalar dependencias (asumiendo que requirements.txt está un nivel arriba)
# Ajusta la ruta a ../requirements.txt o ./requirements.txt según dónde lo hayas guardado
if [ -f "../requirements.txt" ]; then
    echo "📥 Syncing dependencies with uv..."
    uv pip install -r ../requirements.txt
else
    echo "⚠️ No requirements.txt found. Skipping dependency installation."
fi

# 5. Ejecutar el simulador
echo "🎯 Launching the exam simulator..."
python run_browser_exam.py