"""
Excepciones personalizadas para validación de datos en GIC.
Cada excepción hereda de una clase base para manejo centralizado.
"""


class GICValidationError(Exception):
    """Clase base para errores de validación del sistema GIC."""

    def __init__(self, mensaje: str, campo: str = ""):
        self.mensaje = mensaje
        self.campo = campo
        super().__init__(self.mensaje)

    def __str__(self):
        if self.campo:
            return f"[{self.campo}] {self.mensaje}"
        return self.mensaje


class EmailInvalidoError(GICValidationError):
    """Se lanza cuando un email no cumple el formato válido."""

    def __init__(self, mensaje: str = "Email inválido"):
        super().__init__(mensaje, campo="email")


class TelefonoInvalidoError(GICValidationError):
    """Se lanza cuando un teléfono no es válido."""

    def __init__(self, mensaje: str = "Teléfono inválido"):
        super().__init__(mensaje, campo="telefono")


class DireccionInvalidaError(GICValidationError):
    """Se lanza cuando una dirección no cumple los requisitos."""

    def __init__(self, mensaje: str = "Dirección inválida"):
        super().__init__(mensaje, campo="direccion")


class NombreInvalidoError(GICValidationError):
    """Se lanza cuando un nombre no cumple el formato."""

    def __init__(self, mensaje: str = "Nombre inválido"):
        super().__init__(mensaje, campo="nombre")


class RutInvalidoError(GICValidationError):
    """Se lanza cuando un RUT chileno no es válido."""

    def __init__(self, mensaje: str = "RUT inválido"):
        super().__init__(mensaje, campo="rut")
