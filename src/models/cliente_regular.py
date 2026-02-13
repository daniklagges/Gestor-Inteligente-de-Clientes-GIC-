"""
ClienteRegular - Tipo de cliente estándar.

Hereda de Cliente. Tiene descuento base del 0% y un límite de crédito fijo.
Demuestra herencia y uso de super().
"""
from src.models.cliente import Cliente
from src.utils.logger import logger


class ClienteRegular(Cliente):
    """
    Cliente regular con funcionalidades básicas.

    Atributos adicionales:
        _limite_credito (float): Límite de crédito asignado.
        _puntos_fidelidad (int): Puntos acumulados por compras.
    """

    DESCUENTO_BASE = 0.0  # 0%
    LIMITE_CREDITO_DEFAULT = 500_000  # CLP

    def __init__(
        self,
        nombre: str,
        email: str,
        telefono: str,
        direccion: str,
        limite_credito: float = None,
        puntos_fidelidad: int = 0,
        **kwargs,
    ):
        super().__init__(nombre, email, telefono, direccion, **kwargs)
        self._limite_credito = limite_credito or self.LIMITE_CREDITO_DEFAULT
        self._puntos_fidelidad = puntos_fidelidad

        logger.info(f"ClienteRegular inicializado: {self.nombre}")

    # ==================== PROPIEDADES ====================

    @property
    def limite_credito(self) -> float:
        return self._limite_credito

    @property
    def puntos_fidelidad(self) -> int:
        return self._puntos_fidelidad

    @property
    def tipo_cliente(self) -> str:
        """Sobrescribe tipo_cliente del padre (polimorfismo)."""
        return "Regular"

    # ==================== MÉTODOS ====================

    def agregar_puntos(self, puntos: int):
        """Agrega puntos de fidelidad."""
        if puntos < 0:
            raise ValueError("Los puntos no pueden ser negativos")
        self._puntos_fidelidad += puntos
        logger.info(f"Puntos agregados a {self.nombre}: +{puntos} (Total: {self._puntos_fidelidad})")

    def calcular_descuento(self, monto: float) -> float:
        """
        Calcula descuento para cliente regular.
        Sin descuento base, pero 1% extra cada 1000 puntos (máx 5%).
        """
        descuento_puntos = min((self._puntos_fidelidad // 1000) * 0.01, 0.05)
        descuento_total = self.DESCUENTO_BASE + descuento_puntos
        return round(monto * descuento_total, 2)

    def to_dict(self) -> dict:
        """Extiende serialización del padre con atributos propios."""
        datos = super().to_dict()
        datos.update({
            "limite_credito": self._limite_credito,
            "puntos_fidelidad": self._puntos_fidelidad,
        })
        return datos

    @classmethod
    def from_dict(cls, datos: dict) -> "ClienteRegular":
        return cls(
            nombre=datos["nombre"],
            email=datos["email"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            id=datos.get("id"),
            activo=datos.get("activo", True),
            fecha_registro=datos.get("fecha_registro"),
            limite_credito=datos.get("limite_credito"),
            puntos_fidelidad=datos.get("puntos_fidelidad", 0),
        )

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} | Puntos: {self._puntos_fidelidad}"
