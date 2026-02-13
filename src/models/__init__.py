from src.models.cliente import Cliente
from src.models.cliente_regular import ClienteRegular
from src.models.cliente_premium import ClientePremium
from src.models.cliente_corporativo import ClienteCorporativo

# Factory para crear clientes según tipo
TIPOS_CLIENTE = {
    "Regular": ClienteRegular,
    "Premium": ClientePremium,
    "Corporativo": ClienteCorporativo,
}


def crear_cliente(tipo: str, **kwargs) -> Cliente:
    """
    Factory method para crear clientes según tipo.
    Uso: crear_cliente("Premium", nombre="Juan", email="j@mail.com", ...)
    """
    clase = TIPOS_CLIENTE.get(tipo)
    if not clase:
        raise ValueError(
            f"Tipo de cliente inválido: '{tipo}'. "
            f"Opciones: {list(TIPOS_CLIENTE.keys())}"
        )
    return clase(**kwargs)
