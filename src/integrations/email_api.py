import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from src.utils.logger import logger
from src.exceptions.api_errors import APIExternaError


def enviar_email_bienvenida(nombre, email_destino, tipo_cliente):
    smtp_user = Config.SMTP_USER
    if not smtp_user or smtp_user == "tu_email@gmail.com":
        logger.info(f"Email simulado para: {email_destino}")
        return {"enviado": True, "mensaje": f"[SIMULADO] Email enviado a {email_destino}"}
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Bienvenido/a a SolutionTech, {nombre}!"
        msg["From"] = smtp_user
        msg["To"] = email_destino
        html = f"<html><body><h2>Bienvenido/a, {nombre}!</h2><p>Tu cuenta como cliente <strong>{tipo_cliente}</strong> ha sido creada.</p></body></html>"
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(smtp_user, Config.SMTP_PASSWORD)
            server.send_message(msg)
        return {"enviado": True, "mensaje": f"Email enviado a {email_destino}"}
    except smtplib.SMTPException as e:
        raise APIExternaError("SMTP Email", str(e))
    except Exception as e:
        return {"enviado": False, "mensaje": str(e)}
