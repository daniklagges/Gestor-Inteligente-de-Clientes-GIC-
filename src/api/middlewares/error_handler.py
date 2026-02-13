from flask import jsonify
from src.utils.logger import logger


def registrar_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"ok": False, "error": "Solicitud invalida"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"ok": False, "error": "Recurso no encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Error interno: {error}")
        return jsonify({"ok": False, "error": "Error interno del servidor"}), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Excepcion no manejada: {error}")
        return jsonify({"ok": False, "error": str(error)}), 500
