from flask import Blueprint, jsonify, request
from src.services.cliente_service import ClienteService
from src.exceptions.validation_errors import GICValidationError
from src.exceptions.database_errors import RegistroNoEncontradoError, RegistroDuplicadoError
from src.utils.logger import logger

cliente_bp = Blueprint("clientes", __name__)


def get_service():
    return ClienteService()


@cliente_bp.route("", methods=["GET"])
def listar_clientes():
    tipo = request.args.get("tipo")
    activos = request.args.get("activos", "false").lower() == "true"
    busqueda = request.args.get("busqueda")
    clientes = get_service().listar_clientes(activos_solo=activos, tipo=tipo, busqueda=busqueda)
    return jsonify({"ok": True, "total": len(clientes), "clientes": [c.to_dict() for c in clientes]})


@cliente_bp.route("/<id>", methods=["GET"])
def obtener_cliente(id):
    try:
        cliente = get_service().obtener_cliente(id)
        return jsonify({"ok": True, "cliente": cliente.to_dict()})
    except RegistroNoEncontradoError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@cliente_bp.route("", methods=["POST"])
def crear_cliente():
    datos = request.get_json()
    if not datos:
        return jsonify({"ok": False, "error": "Se requiere body JSON"}), 400
    tipo = datos.pop("tipo", "Regular")
    try:
        cliente = get_service().crear_cliente(tipo, **datos)
        return jsonify({"ok": True, "mensaje": "Cliente creado", "cliente": cliente.to_dict()}), 201
    except GICValidationError as e:
        return jsonify({"ok": False, "error": str(e), "campo": e.campo}), 422
    except RegistroDuplicadoError as e:
        return jsonify({"ok": False, "error": str(e)}), 409
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@cliente_bp.route("/<id>", methods=["PUT"])
def actualizar_cliente(id):
    datos = request.get_json()
    if not datos:
        return jsonify({"ok": False, "error": "Se requiere body JSON"}), 400
    try:
        cliente = get_service().actualizar_cliente(id, **datos)
        return jsonify({"ok": True, "mensaje": "Cliente actualizado", "cliente": cliente.to_dict()})
    except RegistroNoEncontradoError as e:
        return jsonify({"ok": False, "error": str(e)}), 404
    except GICValidationError as e:
        return jsonify({"ok": False, "error": str(e)}), 422


@cliente_bp.route("/<id>", methods=["DELETE"])
def eliminar_cliente(id):
    try:
        get_service().eliminar_cliente(id)
        return jsonify({"ok": True, "mensaje": "Cliente eliminado"})
    except RegistroNoEncontradoError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@cliente_bp.route("/<id>/toggle", methods=["PATCH"])
def toggle_cliente(id):
    try:
        service = get_service()
        cliente = service.obtener_cliente(id)
        if cliente.activo:
            service.desactivar_cliente(id)
            estado = "desactivado"
        else:
            cliente.activar()
            from src.repositories.sqlite_repository import SQLiteRepository
            SQLiteRepository().actualizar(cliente)
            estado = "activado"
        return jsonify({"ok": True, "mensaje": f"Cliente {estado}"})
    except RegistroNoEncontradoError as e:
        return jsonify({"ok": False, "error": str(e)}), 404


@cliente_bp.route("/stats", methods=["GET"])
def estadisticas():
    stats = get_service().estadisticas()
    return jsonify({"ok": True, "estadisticas": stats})


@cliente_bp.route("/export/json", methods=["POST"])
def exportar_json():
    ruta = get_service().exportar_json()
    return jsonify({"ok": True, "mensaje": "Exportado a JSON", "ruta": ruta})


@cliente_bp.route("/export/csv", methods=["POST"])
def exportar_csv():
    ruta = get_service().exportar_csv()
    return jsonify({"ok": True, "mensaje": "Exportado a CSV", "ruta": ruta})
