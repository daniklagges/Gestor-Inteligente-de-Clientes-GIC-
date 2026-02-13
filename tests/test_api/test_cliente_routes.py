import pytest
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.api.app import create_app
from src.database.connection import DatabaseConnection


@pytest.fixture(autouse=True)
def limpiar_bd():
    with DatabaseConnection() as conn:
        conn.execute("DELETE FROM clientes")
        conn.commit()
    yield
    with DatabaseConnection() as conn:
        conn.execute("DELETE FROM clientes")
        conn.commit()


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


_counter = 0

def crear_regular(client, nombre="Test User", email=None):
    global _counter
    _counter += 1
    if not email:
        email = f"test{_counter}@example.com"
    return client.post("/api/clientes",
        data=json.dumps({
            "tipo": "Regular",
            "nombre": nombre,
            "email": email,
            "telefono": "+56944556677",
            "direccion": "Calle Test 123 Santiago",
        }), content_type="application/json")


class TestHealthRoutes:

    def test_home(self, client):
        resp = client.get("/")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["sistema"] == "Gestor Inteligente de Clientes (GIC)"

    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "ok"


class TestCrearCliente:

    def test_crear_regular(self, client):
        resp = crear_regular(client)
        data = resp.get_json()
        assert resp.status_code == 201
        assert data["ok"] is True
        assert data["cliente"]["nombre"] == "Test User"
        assert data["cliente"]["tipo_cliente"] == "Regular"

    def test_crear_premium(self, client):
        resp = client.post("/api/clientes",
            data=json.dumps({
                "tipo": "Premium",
                "nombre": "Premium User",
                "email": "premium_unique@test.com",
                "telefono": "+56955667788",
                "direccion": "Av Premium 456 Providencia",
                "nivel_premium": "Platinum",
            }), content_type="application/json")
        data = resp.get_json()
        assert resp.status_code == 201
        assert data["cliente"]["tipo_cliente"] == "Premium"
        assert data["cliente"]["nivel_premium"] == "Platinum"

    def test_crear_corporativo(self, client):
        resp = client.post("/api/clientes",
            data=json.dumps({
                "tipo": "Corporativo",
                "nombre": "Corp User",
                "email": "corp_unique@empresa.cl",
                "telefono": "+56966778899",
                "direccion": "Apoquindo 1000 Las Condes",
                "rut_empresa": "76.124.890-1",
                "razon_social": "TestCorp SpA",
                "cantidad_empleados": 50,
            }), content_type="application/json")
        data = resp.get_json()
        assert resp.status_code == 201
        assert data["cliente"]["tipo_cliente"] == "Corporativo"

    def test_crear_sin_body(self, client):
        resp = client.post("/api/clientes", content_type="application/json")
        assert resp.status_code == 400

    def test_crear_email_invalido(self, client):
        resp = client.post("/api/clientes",
            data=json.dumps({
                "tipo": "Regular",
                "nombre": "Bad Email",
                "email": "no-valido",
                "telefono": "+56944556677",
                "direccion": "Direccion 123",
            }), content_type="application/json")
        assert resp.status_code == 422

    def test_crear_email_duplicado(self, client):
        crear_regular(client, email="dup@test.com")
        resp = crear_regular(client, email="dup@test.com")
        assert resp.status_code == 409


class TestListarClientes:

    def test_listar_vacio(self, client):
        resp = client.get("/api/clientes")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["ok"] is True
        assert data["total"] == 0

    def test_listar_con_datos(self, client):
        crear_regular(client)
        resp = client.get("/api/clientes")
        data = resp.get_json()
        assert data["total"] == 1

    def test_filtrar_por_tipo(self, client):
        crear_regular(client)
        resp = client.get("/api/clientes?tipo=Premium")
        assert resp.get_json()["total"] == 0
        resp = client.get("/api/clientes?tipo=Regular")
        assert resp.get_json()["total"] == 1

    def test_busqueda(self, client):
        crear_regular(client, nombre="Danissa Klagges")
        resp = client.get("/api/clientes?busqueda=Danissa")
        assert resp.get_json()["total"] == 1
        resp = client.get("/api/clientes?busqueda=noexiste")
        assert resp.get_json()["total"] == 0


class TestObtenerCliente:

    def test_obtener_por_id(self, client):
        resp = crear_regular(client)
        id_cliente = resp.get_json()["cliente"]["id"]
        resp = client.get(f"/api/clientes/{id_cliente}")
        assert resp.status_code == 200
        assert resp.get_json()["ok"] is True

    def test_obtener_no_existe(self, client):
        resp = client.get("/api/clientes/id-falso-123")
        assert resp.status_code == 404


class TestActualizarCliente:

    def test_actualizar_nombre(self, client):
        resp = crear_regular(client)
        id_cliente = resp.get_json()["cliente"]["id"]
        resp = client.put(f"/api/clientes/{id_cliente}",
            data=json.dumps({"nombre": "Nombre Nuevo"}),
            content_type="application/json")
        assert resp.status_code == 200
        assert resp.get_json()["cliente"]["nombre"] == "Nombre Nuevo"

    def test_actualizar_no_existe(self, client):
        resp = client.put("/api/clientes/id-falso",
            data=json.dumps({"nombre": "Test"}),
            content_type="application/json")
        assert resp.status_code == 404


class TestEliminarCliente:

    def test_eliminar(self, client):
        resp = crear_regular(client)
        id_cliente = resp.get_json()["cliente"]["id"]
        resp = client.delete(f"/api/clientes/{id_cliente}")
        assert resp.status_code == 200
        resp = client.get(f"/api/clientes/{id_cliente}")
        assert resp.status_code == 404

    def test_eliminar_no_existe(self, client):
        resp = client.delete("/api/clientes/id-falso")
        assert resp.status_code == 404


class TestToggleCliente:

    def test_desactivar_y_activar(self, client):
        resp = crear_regular(client)
        id_cliente = resp.get_json()["cliente"]["id"]
        resp = client.patch(f"/api/clientes/{id_cliente}/toggle")
        assert resp.status_code == 200
        assert "desactivado" in resp.get_json()["mensaje"]
        resp = client.patch(f"/api/clientes/{id_cliente}/toggle")
        assert "activado" in resp.get_json()["mensaje"]


class TestEstadisticas:

    def test_stats_vacio(self, client):
        resp = client.get("/api/clientes/stats")
        data = resp.get_json()
        assert data["ok"] is True
        assert data["estadisticas"]["total"] == 0

    def test_stats_con_datos(self, client):
        crear_regular(client)
        resp = client.get("/api/clientes/stats")
        assert resp.get_json()["estadisticas"]["total"] == 1


class TestExportar:

    def test_exportar_json(self, client):
        crear_regular(client)
        resp = client.post("/api/clientes/export/json")
        assert resp.status_code == 200
        assert resp.get_json()["ok"] is True

    def test_exportar_csv(self, client):
        crear_regular(client)
        resp = client.post("/api/clientes/export/csv")
        assert resp.status_code == 200
        assert resp.get_json()["ok"] is True
