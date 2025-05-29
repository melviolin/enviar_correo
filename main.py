import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/enviar", methods=["POST"])
def enviar():
    print("Inicio de la función enviar()")

    data = request.get_json()
    print("Datos recibidos:", data)

    destinatario = data.get("to")
    asunto = data.get("subject")
    mensaje_html = data.get("html")

    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    print(f"SMTP Config -> user: {smtp_user}, server: {smtp_server}, port: {smtp_port}")

    return jsonify({
        "destinatario": destinatario,
        "asunto": asunto,
        "mensaje": mensaje_html,
        "user": smtp_user,
        "pass": smtp_pass,
        "server": smtp_server,
        "port": smtp_port
    }), 400

    mensaje = MIMEMultipart()
    mensaje["From"] = smtp_user
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.attach(MIMEText(mensaje_html, "html"))

    try:
        print("Conectando al servidor SMTP...")
        with smtplib.SMTP(smtp_server, smtp_port) as servidor:
            print("Iniciando TLS...")
            servidor.starttls()
            print("Haciendo login...")
            servidor.login(smtp_user, smtp_pass)
            print("Enviando mensaje...")
            servidor.send_message(mensaje)
            print("Correo enviado con éxito")
            return jsonify({"status": "ok", "message": "Correo enviado"})
    except Exception as e:
        print("Error enviando correo:", e)
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
