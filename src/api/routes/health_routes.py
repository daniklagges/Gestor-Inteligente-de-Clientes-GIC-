from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "sistema": "Gestor Inteligente de Clientes (GIC)",
        "version": "1.0.0",
        "estado": "activo",
    })


@health_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200
