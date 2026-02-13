"""
Repositorio CSV - Exportación/importación de clientes en formato CSV.
"""
import csv
import os
from typing import List
from src.models import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo
from src.utils.logger import logger

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


class CSVRepository:
    """Repositorio para leer/escribir clientes en archivos CSV."""

    _CLASES = {
        "Regular": ClienteRegular,
        "Premium": ClientePremium,
        "Corporativo": ClienteCorporativo,
    }

    def __init__(self, archivo: str = "clientes.csv"):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.ruta = os.path.join(DATA_DIR, archivo)

    def exportar(self, clientes: List[Cliente]) -> str:
        """Exporta lista de clientes a archivo CSV."""
        if not clientes:
            logger.warning("No hay clientes para exportar")
            return self.ruta

        datos = [c.to_dict() for c in clientes]

        # Recopilar todos los campos posibles de todos los clientes
        campos = []
        for d in datos:
            for k in d.keys():
                if k not in campos:
                    campos.append(k)

        with open(self.ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(datos)

        logger.info(f"Exportados {len(clientes)} clientes a CSV: {self.ruta}")
        return self.ruta

    def importar(self) -> List[Cliente]:
        """Importa clientes desde archivo CSV."""
        if not os.path.exists(self.ruta):
            logger.warning(f"Archivo CSV no encontrado: {self.ruta}")
            return []

        clientes = []
        with open(self.ruta, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convertir strings a tipos apropiados
                row["activo"] = row.get("activo", "True").lower() in ("true", "1")
                for campo in ("limite_credito", "descuento", "descuento_volumen"):
                    if campo in row and row[campo]:
                        row[campo] = float(row[campo])
                for campo in ("puntos_fidelidad", "cantidad_empleados"):
                    if campo in row and row[campo]:
                        row[campo] = int(row[campo])

                tipo = row.get("tipo_cliente", "Regular")
                clase = self._CLASES.get(tipo, ClienteRegular)
                clientes.append(clase.from_dict(row))

        logger.info(f"Importados {len(clientes)} clientes desde CSV")
        return clientes
