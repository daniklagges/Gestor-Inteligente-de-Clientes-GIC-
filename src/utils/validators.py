"""
Módulo de validaciones avanzadas para el proyecto GIC.
Valida email, teléfono y dirección usando librerías especializadas.
"""
import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from src.exceptions.validation_errors import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    DireccionInvalidaError,
    NombreInvalidoError,
    RutInvalidoError,
)


def validar_email(email: str) -> str:
    """
    Valida formato de email usando email-validator.
    Retorna el email normalizado si es válido.
    Lanza EmailInvalidoError si no es válido.
    """
    try:
        resultado = validate_email(email, check_deliverability=False)
        return resultado.normalized
    except EmailNotValidError as e:
        raise EmailInvalidoError(f"Email inválido '{email}': {str(e)}")


def validar_telefono(telefono: str, region: str = "CL") -> str:
    """
    Valida número de teléfono usando phonenumbers.
    Retorna el teléfono en formato internacional.
    Lanza TelefonoInvalidoError si no es válido.
    """
    try:
        numero = phonenumbers.parse(telefono, region)
        if not phonenumbers.is_valid_number(numero):
            raise TelefonoInvalidoError(
                f"Teléfono inválido '{telefono}' para región {region}"
            )
        return phonenumbers.format_number(
            numero, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
    except phonenumbers.NumberParseException as e:
        raise TelefonoInvalidoError(f"No se pudo parsear '{telefono}': {str(e)}")


def validar_direccion(direccion: str) -> str:
    """
    Valida que la dirección no esté vacía y tenga un largo mínimo.
    Retorna la dirección limpia.
    """
    direccion = direccion.strip()
    if not direccion:
        raise DireccionInvalidaError("La dirección no puede estar vacía")
    if len(direccion) < 5:
        raise DireccionInvalidaError(
            "La dirección debe tener al menos 5 caracteres"
        )
    return direccion


def validar_nombre(nombre: str) -> str:
    """
    Valida que el nombre solo contenga letras, espacios y tildes.
    Retorna el nombre limpio con capitalización.
    """
    nombre = nombre.strip()
    if not nombre:
        raise NombreInvalidoError("El nombre no puede estar vacío")
    if len(nombre) < 2:
        raise NombreInvalidoError("El nombre debe tener al menos 2 caracteres")
    patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$"
    if not re.match(patron, nombre):
        raise NombreInvalidoError(
            "El nombre solo puede contener letras, espacios y tildes"
        )
    return nombre.title()


def validar_rut(rut: str) -> str:
    """
    Valida RUT chileno (formato XX.XXX.XXX-X o XXXXXXXX-X).
    Retorna el RUT formateado.
    """
    rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()

    if len(rut_limpio) < 2:
        raise RutInvalidoError("RUT demasiado corto")

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    if not cuerpo.isdigit():
        raise RutInvalidoError(f"RUT inválido: '{rut}'")

    # Cálculo del dígito verificador
    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = multiplicador + 1 if multiplicador < 7 else 2

    resto = suma % 11
    dv_calculado = str(11 - resto)

    if dv_calculado == "11":
        dv_calculado = "0"
    elif dv_calculado == "10":
        dv_calculado = "K"

    if dv != dv_calculado:
        raise RutInvalidoError(f"Dígito verificador incorrecto para RUT '{rut}'")

    # Formatear
    cuerpo_formateado = f"{int(cuerpo):,}".replace(",", ".")
    return f"{cuerpo_formateado}-{dv_calculado}"
