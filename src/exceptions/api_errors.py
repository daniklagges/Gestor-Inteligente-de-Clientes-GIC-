"""
Excepciones personalizadas para integraciones con APIs externas.
"""


class GICAPIError(Exception):
    """Clase base para errores de API externa."""

    def __init__(self, mensaje: str = "Error en API externa", codigo: int = 0):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(self.mensaje)


class APIExternaError(GICAPIError):
    """Se lanza cuando una API externa retorna un error."""

    def __init__(self, servicio: str = "", mensaje: str = "", codigo: int = 0):
        msg = f"Error en servicio '{servicio}': {mensaje}"
        super().__init__(msg, codigo)


class APITimeoutError(GICAPIError):
    """Se lanza cuando una API externa no responde a tiempo."""

    def __init__(self, servicio: str = "", timeout: int = 0):
        mensaje = f"Timeout ({timeout}s) al conectar con '{servicio}'"
        super().__init__(mensaje)
