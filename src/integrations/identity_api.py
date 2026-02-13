import requests
from config import Config
from src.exceptions.api_errors import APIExternaError, APITimeoutError
from src.utils.logger import logger


def validar_identidad(nombre, email, rut=""):
    api_url = Config.IDENTITY_API_URL
    if not api_url or api_url == "https://api.example.com/validate":
        logger.info("Validacion de identidad local (sin API externa)")
        return _validacion_local(nombre, email, rut)
    try:
        response = requests.post(api_url,
            json={"nombre": nombre, "email": email, "rut": rut},
            headers={"Authorization": f"Bearer {Config.IDENTITY_API_KEY}"},
            timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {"valido": data.get("valid", False), "mensaje": data.get("message", ""), "score": data.get("score", 0.0)}
        else:
            raise APIExternaError("Identity API", f"Status {response.status_code}", response.status_code)
    except requests.Timeout:
        raise APITimeoutError("Identity API", 10)
    except requests.RequestException:
        return _validacion_local(nombre, email, rut)


def _validacion_local(nombre, email, rut=""):
    score = 0.0
    if nombre and len(nombre) >= 3:
        score += 0.3
    if email and "@" in email:
        score += 0.4
    if rut and len(rut) >= 9:
        score += 0.3
    return {"valido": score >= 0.7, "mensaje": "Validacion local", "score": round(score, 2)}
