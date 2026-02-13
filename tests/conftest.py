"""
Configuración global de pytest para el proyecto GIC.
"""
import sys
import os

# Asegurar que el directorio raíz esté en el path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
