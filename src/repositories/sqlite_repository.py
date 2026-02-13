"""
Repositorio SQLite - Capa de persistencia para clientes.
Implementa el patrón Repository para desacoplar lógica de negocio de la BD.
"""
from typing import List, Optional
from src.database.connection import DatabaseConnection
from src.models import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo
from src.exceptions.database_errors import (
    RegistroNoEncontradoError,
    RegistroDuplicadoError,
)
from src.utils.logger import logger
from src.utils.helpers import timestamp_actual
import sqlite3


class SQLiteRepository:
    """Repositorio para operaciones CRUD de clientes en SQLite."""

    # Mapeo tipo_cliente -> clase
    _CLASES = {
        "Regular": ClienteRegular,
        "Premium": ClientePremium,
        "Corporativo": ClienteCorporativo,
    }

    def crear(self, cliente: Cliente) -> Cliente:
        """Inserta un nuevo cliente en la BD."""
        datos = cliente.to_dict()
        columnas = ", ".join(datos.keys())
        placeholders = ", ".join(["?"] * len(datos))

        try:
            with DatabaseConnection() as conn:
                conn.execute(
                    f"INSERT INTO clientes ({columnas}) VALUES ({placeholders})",
                    list(datos.values()),
                )
                logger.info(f"Cliente guardado en BD: {cliente.nombre} ({cliente.id})")
                return cliente
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: clientes.email" in str(e):
                raise RegistroDuplicadoError("email", cliente.email)
            raise

    def obtener_por_id(self, id: str) -> Cliente:
        """Busca un cliente por su ID."""
        with DatabaseConnection() as conn:
            row = conn.execute(
                "SELECT * FROM clientes WHERE id = ?", (id,)
            ).fetchone()

        if not row:
            raise RegistroNoEncontradoError("Cliente", id)

        return self._row_to_cliente(dict(row))

    def obtener_por_email(self, email: str) -> Optional[Cliente]:
        """Busca un cliente por su email."""
        with DatabaseConnection() as conn:
            row = conn.execute(
                "SELECT * FROM clientes WHERE email = ?", (email,)
            ).fetchone()

        if not row:
            return None
        return self._row_to_cliente(dict(row))

    def listar(
        self,
        activos_solo: bool = False,
        tipo: str = None,
        busqueda: str = None,
    ) -> List[Cliente]:
        """Lista clientes con filtros opcionales."""
        query = "SELECT * FROM clientes WHERE 1=1"
        params = []

        if activos_solo:
            query += " AND activo = 1"
        if tipo:
            query += " AND tipo_cliente = ?"
            params.append(tipo)
        if busqueda:
            query += " AND (nombre LIKE ? OR email LIKE ? OR telefono LIKE ?)"
            patron = f"%{busqueda}%"
            params.extend([patron, patron, patron])

        query += " ORDER BY fecha_registro DESC"

        with DatabaseConnection() as conn:
            rows = conn.execute(query, params).fetchall()

        return [self._row_to_cliente(dict(row)) for row in rows]

    def actualizar(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente existente."""
        datos = cliente.to_dict()
        datos["fecha_actualizacion"] = timestamp_actual()

        sets = ", ".join([f"{k} = ?" for k in datos.keys() if k != "id"])
        valores = [v for k, v in datos.items() if k != "id"]
        valores.append(datos["id"])

        with DatabaseConnection() as conn:
            cursor = conn.execute(
                f"UPDATE clientes SET {sets} WHERE id = ?", valores
            )
            if cursor.rowcount == 0:
                raise RegistroNoEncontradoError("Cliente", datos["id"])

        logger.info(f"Cliente actualizado: {cliente.nombre} ({cliente.id})")
        return cliente

    def eliminar(self, id: str) -> bool:
        """Elimina un cliente de la BD (borrado físico)."""
        with DatabaseConnection() as conn:
            cursor = conn.execute("DELETE FROM clientes WHERE id = ?", (id,))
            if cursor.rowcount == 0:
                raise RegistroNoEncontradoError("Cliente", id)

        logger.info(f"Cliente eliminado de BD: {id}")
        return True

    def desactivar(self, id: str) -> bool:
        """Desactiva un cliente (borrado lógico)."""
        with DatabaseConnection() as conn:
            cursor = conn.execute(
                "UPDATE clientes SET activo = 0, fecha_actualizacion = ? WHERE id = ?",
                (timestamp_actual(), id),
            )
            if cursor.rowcount == 0:
                raise RegistroNoEncontradoError("Cliente", id)

        logger.info(f"Cliente desactivado: {id}")
        return True

    def contar(self, tipo: str = None) -> int:
        """Cuenta clientes, opcionalmente por tipo."""
        query = "SELECT COUNT(*) FROM clientes"
        params = []
        if tipo:
            query += " WHERE tipo_cliente = ?"
            params.append(tipo)

        with DatabaseConnection() as conn:
            row = conn.execute(query, params).fetchone()
        return row[0]

    def _row_to_cliente(self, datos: dict) -> Cliente:
        """Convierte un row de BD a la clase de cliente correspondiente."""
        tipo = datos.get("tipo_cliente", "Regular")
        clase = self._CLASES.get(tipo, ClienteRegular)
        return clase.from_dict(datos)
