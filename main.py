import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/enviar", methods=["POST"])
def enviar():
    data = request.get_json()
    destinatario = data.get("to")
    asunto = data.get("subject")
    mensaje_html = data.get("html")

    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    mensaje = MIMEMultipart()
    mensaje["From"] = smtp_user
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(mensaje_html, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(smtp_user, smtp_pass)
            servidor.send_message(mensaje)
            return jsonify({"status": "ok", "message": "Correo enviado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
