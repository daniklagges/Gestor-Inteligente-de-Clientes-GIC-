"""
Pruebas unitarias para el modelo Cliente y sus subclases.
"""
import pytest
import sys
import os

# Agregar raíz del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.models.cliente import Cliente
from src.models.cliente_regular import ClienteRegular
from src.models.cliente_premium import ClientePremium
from src.models.cliente_corporativo import ClienteCorporativo
from src.exceptions.validation_errors import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    NombreInvalidoError,
)


# ==================== FIXTURES ====================

@pytest.fixture
def cliente_base():
    return Cliente(
        nombre="Juan Pérez",
        email="juan@example.com",
        telefono="+56944556677",
        direccion="Av. Siempre Viva 123, Santiago",
    )


@pytest.fixture
def cliente_regular():
    return ClienteRegular(
        nombre="María López",
        email="maria@example.com",
        telefono="+56955667788",
        direccion="Calle Falsa 456, Temuco",
    )


@pytest.fixture
def cliente_premium():
    return ClientePremium(
        nombre="Carlos Díaz",
        email="carlos@example.com",
        telefono="+56966778899",
        direccion="Los Leones 789, Providencia",
        nivel_premium="Platinum",
    )


@pytest.fixture
def cliente_corporativo():
    return ClienteCorporativo(
        nombre="Ana Muñoz",
        email="ana@empresa.cl",
        telefono="+56977889900",
        direccion="Apoquindo 1000, Las Condes",
        rut_empresa="76.124.890-1",
        razon_social="Empresa Test SpA",
        cantidad_empleados=50,
    )


# ==================== TESTS CLASE BASE ====================

class TestCliente:

    def test_creacion_cliente(self, cliente_base):
        assert cliente_base.nombre == "Juan Pérez"
        assert cliente_base.email == "juan@example.com"
        assert cliente_base.activo is True
        assert cliente_base.tipo_cliente == "Regular"

    def test_email_invalido(self):
        with pytest.raises(EmailInvalidoError):
            Cliente(
                nombre="Test",
                email="no-es-email",
                telefono="+56944556677",
                direccion="Dirección válida 123",
            )

    def test_nombre_invalido(self):
        with pytest.raises(NombreInvalidoError):
            Cliente(
                nombre="",
                email="test@test.com",
                telefono="+56944556677",
                direccion="Dirección válida 123",
            )

    def test_desactivar(self, cliente_base):
        cliente_base.desactivar()
        assert cliente_base.activo is False

    def test_activar(self, cliente_base):
        cliente_base.desactivar()
        cliente_base.activar()
        assert cliente_base.activo is True

    def test_igualdad_por_email(self):
        c1 = Cliente("Juan", "mismo@email.com", "+56944556677", "Dirección 123")
        c2 = Cliente("Pedro", "mismo@email.com", "+56955667788", "Otra dirección 456")
        assert c1 == c2

    def test_to_dict(self, cliente_base):
        datos = cliente_base.to_dict()
        assert datos["nombre"] == "Juan Pérez"
        assert datos["email"] == "juan@example.com"
        assert "id" in datos
        assert "fecha_registro" in datos

    def test_str(self, cliente_base):
        texto = str(cliente_base)
        assert "Juan Pérez" in texto
        assert "Activo" in texto

    def test_calcular_descuento_base(self, cliente_base):
        assert cliente_base.calcular_descuento(100000) == 0.0


# ==================== TESTS CLIENTE REGULAR ====================

class TestClienteRegular:

    def test_creacion(self, cliente_regular):
        assert cliente_regular.tipo_cliente == "Regular"
        assert cliente_regular.puntos_fidelidad == 0
        assert cliente_regular.limite_credito == 500_000

    def test_agregar_puntos(self, cliente_regular):
        cliente_regular.agregar_puntos(500)
        assert cliente_regular.puntos_fidelidad == 500

    def test_puntos_negativos(self, cliente_regular):
        with pytest.raises(ValueError):
            cliente_regular.agregar_puntos(-100)

    def test_descuento_sin_puntos(self, cliente_regular):
        assert cliente_regular.calcular_descuento(100000) == 0.0

    def test_descuento_con_puntos(self, cliente_regular):
        cliente_regular.agregar_puntos(3000)  # 3% descuento
        descuento = cliente_regular.calcular_descuento(100000)
        assert descuento == 3000.0  # 3% de 100.000


# ==================== TESTS CLIENTE PREMIUM ====================

class TestClientePremium:

    def test_creacion(self, cliente_premium):
        assert cliente_premium.tipo_cliente == "Premium"
        assert cliente_premium.nivel_premium == "Platinum"
        assert cliente_premium.descuento == 0.15

    def test_nivel_invalido(self):
        with pytest.raises(ValueError):
            ClientePremium(
                nombre="Test",
                email="test@test.com",
                telefono="+56944556677",
                direccion="Dirección 123",
                nivel_premium="SuperMega",
            )

    def test_descuento_gold(self):
        c = ClientePremium(
            nombre="Test Gold",
            email="gold@test.com",
            telefono="+56944556677",
            direccion="Dirección 123",
            nivel_premium="Gold",
        )
        assert c.calcular_descuento(100000) == 10000.0

    def test_descuento_diamond(self):
        c = ClientePremium(
            nombre="Test Diamond",
            email="diamond@test.com",
            telefono="+56944556677",
            direccion="Dirección 123",
            nivel_premium="Diamond",
        )
        assert c.calcular_descuento(100000) == 20000.0

    def test_subir_nivel(self, cliente_premium):
        # Platinum -> Diamond
        cliente_premium.subir_nivel()
        assert cliente_premium.nivel_premium == "Diamond"
        assert cliente_premium.descuento == 0.20


# ==================== TESTS CLIENTE CORPORATIVO ====================

class TestClienteCorporativo:

    def test_creacion(self, cliente_corporativo):
        assert cliente_corporativo.tipo_cliente == "Corporativo"
        assert cliente_corporativo.razon_social == "Empresa Test SpA"
        assert "76.124.890-1" in cliente_corporativo.rut_empresa

    def test_descuento_por_empleados(self, cliente_corporativo):
        # 50 empleados = 10%
        assert cliente_corporativo.calcular_descuento(100000) == 10000.0

    def test_actualizar_empleados(self, cliente_corporativo):
        cliente_corporativo.actualizar_empleados(250)
        assert cliente_corporativo.cantidad_empleados == 250
        assert cliente_corporativo.descuento_volumen == 0.20


# ==================== TESTS POLIMORFISMO ====================

class TestPolimorfismo:

    def test_calcular_descuento_polimorfico(
        self, cliente_regular, cliente_premium, cliente_corporativo
    ):
        """Verifica que calcular_descuento() se comporta diferente según tipo."""
        monto = 100000
        clientes = [cliente_regular, cliente_premium, cliente_corporativo]
        descuentos = [c.calcular_descuento(monto) for c in clientes]

        # Regular sin puntos = 0, Premium Platinum = 15000, Corp 50emp = 10000
        assert descuentos[0] == 0.0
        assert descuentos[1] == 15000.0
        assert descuentos[2] == 10000.0

    def test_tipo_cliente_polimorfico(
        self, cliente_regular, cliente_premium, cliente_corporativo
    ):
        assert cliente_regular.tipo_cliente == "Regular"
        assert cliente_premium.tipo_cliente == "Premium"
        assert cliente_corporativo.tipo_cliente == "Corporativo"
