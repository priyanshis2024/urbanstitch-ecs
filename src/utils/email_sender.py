from email.mime.text import MIMEText
import aiosmtplib
from fastapi import HTTPException
from src.core.config import settings
from src.utils.constants import SmtpServerTimeout, ErrorMessage, EmailSubjects
from src.exceptions.user_authentication import FailedMail
from email.message import EmailMessage


async def send_otp_email(email: str, otp: str):
    body = f"Your OTP code is: {otp}"

    message = MIMEText(body)
    message["Subject"] = EmailSubjects.OTP_SUBJECT
    message["From"] = settings.SENDER_EMAIL
    message["To"] = email

    try:
        async with aiosmtplib.SMTP(
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            timeout=SmtpServerTimeout.TIMEOUT,
            use_tls=True,
        ) as server:
            await server.login(settings.SENDER_EMAIL, settings.SMTP_PASSWORD)
            await server.send_message(message)

    except Exception as e:
        raise FailedMail(message=ErrorMessage.FAILED_SENDING_EMAIL.format())


async def send_order_email(email: str, html_body: str):

    msg = EmailMessage()
    msg["From"] = settings.SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = EmailSubjects.ORDER_INVOICE_SUBJECT
    msg.add_alternative(html_body, subtype="html")

    try:
        async with aiosmtplib.SMTP(
            hostname=settings.SMTP_SERVER,
            port=settings.SMTP_PORT,
            timeout=SmtpServerTimeout.TIMEOUT,
            use_tls=True,
        ) as server:
            await server.login(settings.SENDER_EMAIL, settings.SMTP_PASSWORD)
            await server.send_message(msg)
    except Exception as e:
        raise FailedMail(message=ErrorMessage.FAILED_SENDING_EMAIL.format())
