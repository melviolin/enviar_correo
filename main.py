import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI
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
        smtp_user = "contacto@melviolin.com"
        smtp_pass = "ZkND#xgjKLdY"
        smtp_server = "melviolin.com"
        smtp_port = 465  # entero

        mensaje = MIMEMultipart()
        mensaje["From"] = smtp_user
        mensaje["To"] = data.to
        mensaje["Subject"] = data.subject
        mensaje.attach(MIMEText(data.html, "html"))

        # Usar SMTP_SSL para puerto 465
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15) as servidor:
            servidor.login(smtp_user, smtp_pass)
            servidor.send_message(mensaje)

        return {"status": "ok", "message": "Correo enviado"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
