from flask_mail import Message
from flask import current_app

from extensions import mail


def send_email(recipient, subject, body):
    try:
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body,
            sender=current_app.config.get("MAIL_DEFAULT_SENDER")
        )

        mail.send(msg)

        print("Email sent successfully to:", recipient)
        return True

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False
