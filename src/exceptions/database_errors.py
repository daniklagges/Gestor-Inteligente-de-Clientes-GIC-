"""
Excepciones personalizadas para operaciones de base de datos en GIC.
"""


class GICDatabaseError(Exception):
    """Clase base para errores de base de datos."""

    def __init__(self, mensaje: str = "Error de base de datos"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ConexionDBError(GICDatabaseError):
    """Se lanza cuando falla la conexión a la base de datos."""

    def __init__(self, mensaje: str = "No se pudo conectar a la base de datos"):
        super().__init__(mensaje)


class RegistroNoEncontradoError(GICDatabaseError):
    """Se lanza cuando no se encuentra un registro."""

    def __init__(self, entidad: str = "Registro", id_registro: str = ""):
        mensaje = f"{entidad} con ID '{id_registro}' no encontrado"
        super().__init__(mensaje)


class RegistroDuplicadoError(GICDatabaseError):
    """Se lanza cuando se intenta crear un registro duplicado."""

    def __init__(self, campo: str = "", valor: str = ""):
        mensaje = f"Ya existe un registro con {campo}='{valor}'"
        super().__init__(mensaje)
