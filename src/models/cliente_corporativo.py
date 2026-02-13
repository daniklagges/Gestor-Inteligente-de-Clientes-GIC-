"""
ClienteCorporativo - Cliente tipo empresa/corporación.

Hereda de Cliente. Tiene RUT empresa, contacto comercial y descuento por volumen.
Demuestra herencia, polimorfismo y composición (datos de empresa dentro del cliente).
"""
from src.models.cliente import Cliente
from src.utils.validators import validar_rut
from src.utils.logger import logger


class ClienteCorporativo(Cliente):
    """
    Cliente corporativo (empresa).

    Atributos adicionales:
        _rut_empresa (str): RUT de la empresa (validado).
        _razon_social (str): Razón social de la empresa.
        _rubro (str): Rubro o giro comercial.
        _contacto_comercial (str): Nombre del contacto en la empresa.
        _cantidad_empleados (int): Número de empleados.
        _descuento_volumen (float): Descuento por volumen de compras.
    """

    DESCUENTO_BASE = 0.05  # 5%

    def __init__(
        self,
        nombre: str,
        email: str,
        telefono: str,
        direccion: str,
        rut_empresa: str,
        razon_social: str,
        rubro: str = "No especificado",
        contacto_comercial: str = "",
        cantidad_empleados: int = 1,
        descuento_volumen: float = None,
        **kwargs,
    ):
        super().__init__(nombre, email, telefono, direccion, **kwargs)
        self._rut_empresa = validar_rut(rut_empresa)
        self._razon_social = razon_social.strip()
        self._rubro = rubro.strip()
        self._contacto_comercial = contacto_comercial.strip()
        self._cantidad_empleados = max(1, cantidad_empleados)
        self._descuento_volumen = descuento_volumen or self._calcular_descuento_volumen()

        logger.info(
            f"ClienteCorporativo inicializado: {self._razon_social} ({self._rut_empresa})"
        )

    # ==================== PROPIEDADES ====================

    @property
    def rut_empresa(self) -> str:
        return self._rut_empresa

    @property
    def razon_social(self) -> str:
        return self._razon_social

    @property
    def rubro(self) -> str:
        return self._rubro

    @property
    def contacto_comercial(self) -> str:
        return self._contacto_comercial

    @contacto_comercial.setter
    def contacto_comercial(self, valor: str):
        self._contacto_comercial = valor.strip()

    @property
    def cantidad_empleados(self) -> int:
        return self._cantidad_empleados

    @property
    def descuento_volumen(self) -> float:
        return self._descuento_volumen

    @property
    def tipo_cliente(self) -> str:
        return "Corporativo"

    # ==================== MÉTODOS ====================

    def _calcular_descuento_volumen(self) -> float:
        """
        Calcula descuento según cantidad de empleados.
        1-10: 5%, 11-50: 10%, 51-200: 15%, 200+: 20%
        """
        if self._cantidad_empleados <= 10:
            return 0.05
        elif self._cantidad_empleados <= 50:
            return 0.10
        elif self._cantidad_empleados <= 200:
            return 0.15
        else:
            return 0.20

    def calcular_descuento(self, monto: float) -> float:
        """
        Calcula descuento corporativo basado en volumen.
        Polimorfismo: sobrescribe el método del padre.
        """
        return round(monto * self._descuento_volumen, 2)

    def actualizar_empleados(self, cantidad: int):
        """Actualiza cantidad de empleados y recalcula descuento."""
        self._cantidad_empleados = max(1, cantidad)
        self._descuento_volumen = self._calcular_descuento_volumen()
        logger.info(
            f"{self._razon_social}: empleados={cantidad}, "
            f"descuento={self._descuento_volumen:.0%}"
        )

    def to_dict(self) -> dict:
        datos = super().to_dict()
        datos.update({
            "rut_empresa": self._rut_empresa,
            "razon_social": self._razon_social,
            "rubro": self._rubro,
            "contacto_comercial": self._contacto_comercial,
            "cantidad_empleados": self._cantidad_empleados,
            "descuento_volumen": self._descuento_volumen,
        })
        return datos

    @classmethod
    def from_dict(cls, datos: dict) -> "ClienteCorporativo":
        return cls(
            nombre=datos["nombre"],
            email=datos["email"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            rut_empresa=datos["rut_empresa"],
            razon_social=datos["razon_social"],
            id=datos.get("id"),
            activo=datos.get("activo", True),
            fecha_registro=datos.get("fecha_registro"),
            rubro=datos.get("rubro", "No especificado"),
            contacto_comercial=datos.get("contacto_comercial", ""),
            cantidad_empleados=datos.get("cantidad_empleados", 1),
            descuento_volumen=datos.get("descuento_volumen"),
        )

    def __str__(self) -> str:
        base = super().__str__()
        return (
            f"{base} | {self._razon_social} | RUT: {self._rut_empresa} | "
            f"Empleados: {self._cantidad_empleados} | "
            f"Dcto: {self._descuento_volumen:.0%}"
        )
