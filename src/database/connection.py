"""
Módulo de conexión a base de datos SQLite.
Implementa context manager para manejo seguro de conexiones.
"""
import sqlite3
import os
from src.utils.logger import logger
from src.exceptions.database_errors import ConexionDBError


class DatabaseConnection:
    """
    Gestiona la conexión a SQLite con context manager.

    Uso:
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
    """

    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.path.join(
            os.path.dirname(__file__), "gic.db"
        )
        self.connection = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Acceso por nombre de columna
            self.connection.execute("PRAGMA foreign_keys = ON")
            return self.connection
        except sqlite3.Error as e:
            logger.error(f"Error al conectar a DB: {e}")
            raise ConexionDBError(f"No se pudo conectar a '{self.db_path}': {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
                logger.error(f"Rollback por error: {exc_val}")
            self.connection.close()
        return False  # No suprimir excepciones
