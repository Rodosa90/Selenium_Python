import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email(sender_email, receiver_email, subject, body, attachment_path, smtp_server, smtp_port, login, password):
    

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar el archivo
    if attachment_path:
        filename = os.path.basename(attachment_path)
        attachment = open(attachment_path, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")

        msg.attach(part)

    # Conectar al servidor SMTP de Outlook y enviar el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            #server.set_debuglevel(1)  # Habilitar modo depuración
            server.starttls()  # Iniciar la conexión TLS (segura)
            server.login(login, password)  # Autenticarse con el servidor SMTP
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Enviar el correo
        print(f"Correo enviado a {receiver_email} con el archivo adjunto {filename}.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")