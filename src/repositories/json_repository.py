"""
Repositorio JSON - Persistencia de clientes en archivos JSON.
Alternativa a SQLite para exportación/importación de datos.
"""
import json
import os
from typing import List
from src.models import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo
from src.utils.logger import logger

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


class JSONRepository:
    """Repositorio para leer/escribir clientes en archivos JSON."""

    _CLASES = {
        "Regular": ClienteRegular,
        "Premium": ClientePremium,
        "Corporativo": ClienteCorporativo,
    }

    def __init__(self, archivo: str = "clientes.json"):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.ruta = os.path.join(DATA_DIR, archivo)

    def exportar(self, clientes: List[Cliente]) -> str:
        """Exporta lista de clientes a archivo JSON."""
        datos = [c.to_dict() for c in clientes]
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

        logger.info(f"Exportados {len(clientes)} clientes a {self.ruta}")
        return self.ruta

    def importar(self) -> List[Cliente]:
        """Importa clientes desde archivo JSON."""
        if not os.path.exists(self.ruta):
            logger.warning(f"Archivo no encontrado: {self.ruta}")
            return []

        with open(self.ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)

        clientes = []
        for item in datos:
            tipo = item.get("tipo_cliente", "Regular")
            clase = self._CLASES.get(tipo, ClienteRegular)
            clientes.append(clase.from_dict(item))

        logger.info(f"Importados {len(clientes)} clientes desde {self.ruta}")
        return clientes
