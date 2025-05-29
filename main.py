import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

class EmailData(BaseModel):
    to: str
    subject: str
    html: str

@app.post("/enviar")
async def enviar_correo(data: EmailData):
    try:
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))

        print("Datos SMTP:", smtp_user, smtp_server, smtp_port)

        mensaje = MIMEMultipart()
        mensaje["From"] = smtp_user
        mensaje["To"] = data.to
        mensaje["Subject"] = data.subject
        mensaje.attach(MIMEText(data.html, "html"))

        with smtplib.SMTP(smtp_server, smtp_port, timeout=15) as servidor:
            servidor.starttls()
            servidor.login(smtp_user, smtp_pass)
            servidor.send_message(mensaje)

        return {"status": "ok", "message": "Correo enviado"}

    except Exception as e:
        print("Error:", str(e))
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
