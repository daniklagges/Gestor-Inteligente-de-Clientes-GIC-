"""
ClientePremium - Cliente con beneficios premium.

Hereda de Cliente. Tiene descuento del 10%, asesor dedicado y prioridad.
Demuestra polimorfismo al sobrescribir calcular_descuento().
"""
from src.models.cliente import Cliente
from src.utils.logger import logger


class ClientePremium(Cliente):
    """
    Cliente premium con beneficios exclusivos.

    Atributos adicionales:
        _descuento (float): Porcentaje de descuento (ej: 0.10 = 10%).
        _asesor_dedicado (str): Nombre del asesor asignado.
        _nivel_premium (str): Nivel premium (Gold, Platinum, Diamond).
    """

    DESCUENTO_BASE = 0.10  # 10%
    NIVELES_VALIDOS = ("Gold", "Platinum", "Diamond")

    def __init__(
        self,
        nombre: str,
        email: str,
        telefono: str,
        direccion: str,
        asesor_dedicado: str = "Sin asignar",
        nivel_premium: str = "Gold",
        descuento: float = None,
        **kwargs,
    ):
        super().__init__(nombre, email, telefono, direccion, **kwargs)

        if nivel_premium not in self.NIVELES_VALIDOS:
            raise ValueError(
                f"Nivel premium inválido: '{nivel_premium}'. "
                f"Opciones: {self.NIVELES_VALIDOS}"
            )

        self._asesor_dedicado = asesor_dedicado
        self._nivel_premium = nivel_premium
        self._descuento = descuento or self._calcular_descuento_por_nivel()

        logger.info(f"ClientePremium [{nivel_premium}] inicializado: {self.nombre}")

    # ==================== PROPIEDADES ====================

    @property
    def asesor_dedicado(self) -> str:
        return self._asesor_dedicado

    @asesor_dedicado.setter
    def asesor_dedicado(self, valor: str):
        self._asesor_dedicado = valor.strip()

    @property
    def nivel_premium(self) -> str:
        return self._nivel_premium

    @property
    def descuento(self) -> float:
        return self._descuento

    @property
    def tipo_cliente(self) -> str:
        return "Premium"

    # ==================== MÉTODOS ====================

    def _calcular_descuento_por_nivel(self) -> float:
        """Asigna descuento según nivel premium."""
        descuentos = {
            "Gold": 0.10,
            "Platinum": 0.15,
            "Diamond": 0.20,
        }
        return descuentos.get(self._nivel_premium, self.DESCUENTO_BASE)

    def subir_nivel(self):
        """Sube al siguiente nivel premium si es posible."""
        niveles = list(self.NIVELES_VALIDOS)
        indice_actual = niveles.index(self._nivel_premium)
        if indice_actual < len(niveles) - 1:
            self._nivel_premium = niveles[indice_actual + 1]
            self._descuento = self._calcular_descuento_por_nivel()
            logger.info(f"{self.nombre} subió a nivel {self._nivel_premium}")
        else:
            logger.warning(f"{self.nombre} ya está en el nivel máximo")

    def calcular_descuento(self, monto: float) -> float:
        """
        Calcula descuento para cliente premium según su nivel.
        Polimorfismo: sobrescribe el método del padre.
        """
        return round(monto * self._descuento, 2)

    def to_dict(self) -> dict:
        datos = super().to_dict()
        datos.update({
            "asesor_dedicado": self._asesor_dedicado,
            "nivel_premium": self._nivel_premium,
            "descuento": self._descuento,
        })
        return datos

    @classmethod
    def from_dict(cls, datos: dict) -> "ClientePremium":
        return cls(
            nombre=datos["nombre"],
            email=datos["email"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            id=datos.get("id"),
            activo=datos.get("activo", True),
            fecha_registro=datos.get("fecha_registro"),
            asesor_dedicado=datos.get("asesor_dedicado", "Sin asignar"),
            nivel_premium=datos.get("nivel_premium", "Gold"),
            descuento=datos.get("descuento"),
        )

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | {self._nivel_premium} | "
            f"Dcto: {self._descuento:.0%} | Asesor: {self._asesor_dedicado}"
        )
