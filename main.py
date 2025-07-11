import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

class EmailData(BaseModel):
    to: str
    subject: str
    html: str
    attachment_base64: str = None  # Base64 opcional
    attachment_name: str = None    # Nombre del archivo adjunto (opcional)

@app.post("/enviar")
async def enviar_correo(data: EmailData):
    try:
        smtp_user = "contacto@melviolin.com"
        smtp_pass = "ZkND#xgjKLdY"
        smtp_server = "melviolin.com"
        smtp_port = 465

        # Multipart: tipo 'mixed' para incluir HTML y adjuntos
        mensaje = MIMEMultipart("mixed")
        mensaje["From"] = smtp_user
        mensaje["To"] = data.to
        mensaje["Bcc"] = smtp_user
        mensaje["Subject"] = data.subject
        mensaje["Reply-To"] = smtp_user

        # Parte alternativa: texto plano y HTML para clientes antiguos
        parte_alternativa = MIMEMultipart("alternative")

        # Texto plano para compatibilidad
        texto_plano = MIMEText("Este correo requiere un visor HTML para mostrarse correctamente.", "plain", "utf-8")
        parte_alternativa.attach(texto_plano)

        # HTML principal
        parte_html = MIMEText(data.html, "html", "utf-8")
        parte_alternativa.attach(parte_html)

        # Adjuntar la parte alternativa (texto/HTML)
        mensaje.attach(parte_alternativa)

        # Si hay adjunto, lo agregamos
        if data.attachment_base64 and data.attachment_name:
            archivo = base64.b64decode(data.attachment_base64)
            parte_adjunto = MIMEApplication(archivo, Name=data.attachment_name)
            parte_adjunto.add_header("Content-Disposition", "attachment", filename=data.attachment_name)
            mensaje.attach(parte_adjunto)

        # Enviar con SMTP seguro
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15) as servidor:
            servidor.login(smtp_user, smtp_pass)
            servidor.send_message(mensaje)

        return {"status": "ok", "message": "Correo enviado"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
