"""
Módulo de logging centralizado para el proyecto GIC.
Usa loguru para registro de actividad del sistema.
"""
import os
from loguru import logger

# Ruta del archivo de log
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "app.log")

# Remover handler por defecto
logger.remove()

# Consola
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{module}</cyan>:<cyan>{function}</cyan> - "
           "<level>{message}</level>",
    level="DEBUG",
)

# Archivo con rotación
logger.add(
    LOG_PATH,
    rotation="5 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {module}:{function} - {message}",
    level="INFO",
)
