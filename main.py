import os
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

import logging
logging.basicConfig(level=logging.DEBUG)


def log(mensaje):
    print(f"[{datetime.datetime.now().isoformat()}] {mensaje}")

@app.route("/enviar", methods=["POST"])
def enviar():
    log("Inicio de la función enviar()")

    data = request.get_json()
    log(f"Datos recibidos: {data}")

    destinatario = data.get("to")
    asunto = data.get("subject")
    mensaje_html = data.get("html")

    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    log(f"SMTP Config -> user: {smtp_user}, server: {smtp_server}, port: {smtp_port}")

    if not all([destinatario, asunto, mensaje_html, smtp_user, smtp_pass, smtp_server]):
        return jsonify({"status": "error", "message": "Faltan datos o configuración SMTP"}), 400

    mensaje = MIMEMultipart()
    mensaje["From"] = smtp_user
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(mensaje_html, "html"))

    try:
        log("Conectando al servidor SMTP...")
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as servidor:
            log("Iniciando TLS...")
            servidor.starttls()
            log("Haciendo login...")
            servidor.login(smtp_user, smtp_pass)
            log("Enviando mensaje...")
            servidor.send_message(mensaje)
            log("Correo enviado con éxito")
            return jsonify({"status": "ok", "message": "Correo enviado"})
    except Exception as e:
        log(f"Error enviando correo: {e}")
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
