# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = FastAPI()

class EmailData(BaseModel):
    to: str
    subject: str
    html: str

@app.post("/send-email")
def send_email(data: EmailData):
    remitente = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    msg = MIMEMultipart("alternative")
    msg["Subject"] = data.subject
    msg["From"] = remitente
    msg["To"] = data.to

    msg.attach(MIMEText(data.html, "html"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, data.to, msg.as_string())
        server.quit()
        return {"status": "enviado"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}
