"""
Clase base Cliente - Modelo principal del sistema GIC.

Implementa:
- Encapsulación con propiedades (getters/setters)
- Validaciones avanzadas en atributos
- Métodos especiales (__str__, __repr__, __eq__)
- Método to_dict() para serialización
"""
from datetime import datetime
from src.utils.helpers import generar_id, timestamp_actual
from src.utils.validators import (
    validar_email,
    validar_telefono,
    validar_direccion,
    validar_nombre,
)
from src.utils.logger import logger


class Cliente:
    """
    Clase base que representa un cliente en el sistema GIC.

    Atributos:
        _id (str): Identificador único del cliente.
        _nombre (str): Nombre completo del cliente.
        _email (str): Correo electrónico validado.
        _telefono (str): Teléfono en formato internacional.
        _direccion (str): Dirección física del cliente.
        _activo (bool): Estado del cliente en el sistema.
        _fecha_registro (str): Timestamp de creación.
        _fecha_actualizacion (str): Timestamp de última actualización.
    """

    def __init__(
        self,
        nombre: str,
        email: str,
        telefono: str,
        direccion: str,
        id: str = None,
        activo: bool = True,
        fecha_registro: str = None,
    ):
        self._id = id or generar_id()
        self._fecha_registro = fecha_registro or timestamp_actual()
        self._fecha_actualizacion = timestamp_actual()
        self._activo = activo

        # Validaciones al asignar (usan los setters con @property)
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.direccion = direccion

        logger.info(f"Cliente creado: {self._nombre} ({self._id})")

    # ==================== PROPIEDADES (Encapsulación) ====================

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = validar_nombre(valor)
        self._fecha_actualizacion = timestamp_actual()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        self._email = validar_email(valor)
        self._fecha_actualizacion = timestamp_actual()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        self._telefono = validar_telefono(valor)
        self._fecha_actualizacion = timestamp_actual()

    @property
    def direccion(self) -> str:
        return self._direccion

    @direccion.setter
    def direccion(self, valor: str):
        self._direccion = validar_direccion(valor)
        self._fecha_actualizacion = timestamp_actual()

    @property
    def activo(self) -> bool:
        return self._activo

    @property
    def fecha_registro(self) -> str:
        return self._fecha_registro

    @property
    def fecha_actualizacion(self) -> str:
        return self._fecha_actualizacion

    @property
    def tipo_cliente(self) -> str:
        """Retorna el tipo de cliente. Sobrescrito por subclases (polimorfismo)."""
        return "Regular"

    # ==================== MÉTODOS DE NEGOCIO ====================

    def activar(self):
        """Activa el cliente en el sistema."""
        self._activo = True
        self._fecha_actualizacion = timestamp_actual()
        logger.info(f"Cliente activado: {self._nombre} ({self._id})")

    def desactivar(self):
        """Desactiva el cliente (borrado lógico)."""
        self._activo = False
        self._fecha_actualizacion = timestamp_actual()
        logger.info(f"Cliente desactivado: {self._nombre} ({self._id})")

    def calcular_descuento(self, monto: float) -> float:
        """
        Calcula el descuento aplicable. Sobrescrito por subclases.
        Cliente base no tiene descuento.
        """
        return 0.0

    def to_dict(self) -> dict:
        """Serializa el cliente a diccionario para persistencia."""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "email": self._email,
            "telefono": self._telefono,
            "direccion": self._direccion,
            "activo": self._activo,
            "tipo_cliente": self.tipo_cliente,
            "fecha_registro": self._fecha_registro,
            "fecha_actualizacion": self._fecha_actualizacion,
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Cliente":
        """Crea una instancia de Cliente desde un diccionario."""
        return cls(
            nombre=datos["nombre"],
            email=datos["email"],
            telefono=datos["telefono"],
            direccion=datos["direccion"],
            id=datos.get("id"),
            activo=datos.get("activo", True),
            fecha_registro=datos.get("fecha_registro"),
        )

    # ==================== MÉTODOS ESPECIALES ====================

    def __str__(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"[{self.tipo_cliente}] {self._nombre} | "
            f"{self._email} | {self._telefono} | {estado}"
        )

    def __repr__(self) -> str:
        return (
            f"Cliente(nombre='{self._nombre}', email='{self._email}', "
            f"id='{self._id}')"
        )

    def __eq__(self, other) -> bool:
        """Dos clientes son iguales si tienen el mismo email."""
        if not isinstance(other, Cliente):
            return NotImplemented
        return self._email == other._email

    def __hash__(self) -> int:
        return hash(self._email)
