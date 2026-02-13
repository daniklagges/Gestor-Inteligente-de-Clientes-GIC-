"""
Funciones auxiliares de uso general para el proyecto GIC.
"""
import uuid
from datetime import datetime


def generar_id() -> str:
    """Genera un ID único basado en UUID4."""
    return str(uuid.uuid4())


def timestamp_actual() -> str:
    """Retorna timestamp actual en formato ISO."""
    return datetime.now().isoformat()


def formatear_fecha(fecha: datetime) -> str:
    """Formatea una fecha a formato legible DD/MM/YYYY HH:MM."""
    return fecha.strftime("%d/%m/%Y %H:%M")
