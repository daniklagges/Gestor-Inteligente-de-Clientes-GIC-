"""
Módulo de migraciones para crear las tablas del sistema GIC.
"""
from src.database.connection import DatabaseConnection
from src.utils.logger import logger


def crear_tablas():
    """Crea todas las tablas necesarias si no existen."""
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # Tabla principal de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                activo INTEGER DEFAULT 1,
                tipo_cliente TEXT NOT NULL DEFAULT 'Regular',
                fecha_registro TEXT NOT NULL,
                fecha_actualizacion TEXT NOT NULL,

                -- Campos ClienteRegular
                limite_credito REAL,
                puntos_fidelidad INTEGER DEFAULT 0,

                -- Campos ClientePremium
                asesor_dedicado TEXT,
                nivel_premium TEXT,
                descuento REAL,

                -- Campos ClienteCorporativo
                rut_empresa TEXT,
                razon_social TEXT,
                rubro TEXT,
                contacto_comercial TEXT,
                cantidad_empleados INTEGER,
                descuento_volumen REAL
            )
        """)

        # Tabla de logs de actividad
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_actividad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                accion TEXT NOT NULL,
                entidad TEXT NOT NULL,
                entidad_id TEXT,
                detalle TEXT,
                fecha TEXT NOT NULL
            )
        """)

        # Índices para búsquedas frecuentes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_clientes_email
            ON clientes(email)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_clientes_tipo
            ON clientes(tipo_cliente)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_clientes_activo
            ON clientes(activo)
        """)

        logger.info("Tablas creadas/verificadas exitosamente")


if __name__ == "__main__":
    crear_tablas()
    print("✅ Base de datos inicializada correctamente")
