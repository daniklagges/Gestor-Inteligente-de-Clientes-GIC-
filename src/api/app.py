"""
Aplicación Flask para la API REST del sistema GIC.
"""
from flask import Flask
from flask_cors import CORS
from src.api.routes.cliente_routes import cliente_bp
from src.api.routes.health_routes import health_bp
from src.api.middlewares.error_handler import registrar_error_handlers
from src.database.migrations import crear_tablas
from config import Config


def create_app():
    """Factory pattern para crear la aplicación Flask."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.FLASK_SECRET_KEY
    CORS(app)
    crear_tablas()
    app.register_blueprint(health_bp)
    app.register_blueprint(cliente_bp, url_prefix="/api/clientes")
    registrar_error_handlers(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=Config.FLASK_PORT, debug=Config.FLASK_DEBUG)
