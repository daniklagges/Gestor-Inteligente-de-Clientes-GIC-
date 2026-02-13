from functools import wraps
from flask import request, jsonify
from config import Config
from src.utils.logger import logger


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return jsonify({"ok": False, "error": "API Key requerida"}), 401
        if api_key != Config.FLASK_SECRET_KEY:
            return jsonify({"ok": False, "error": "API Key invalida"}), 403
        return f(*args, **kwargs)
    return decorated
