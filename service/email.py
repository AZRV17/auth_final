import smtplib
from email.message import EmailMessage
from utils.password_generator import generate_password

SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 465

SENDER_EMAIL = "zlib_sup@inbox.ru"
SENDER_PASSWORD = "aOv3iKgEzuewqI7RXBdf"

def send_email(receiver_email):
    code = generate_password()

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = "Подтверждение регистрации"

    msg.set_content(
        f"""Ваш код для входа:

{code}

Если вы не выполняли регистрацию — проигнорируйте это письмо.
"""
    )

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Ошибка при отправке email:", e)
        raise

    return code
