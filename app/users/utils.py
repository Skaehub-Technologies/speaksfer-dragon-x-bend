from typing import Any
from django.core.mail import send_mail
from django.template.loader import render_to_string
from speaksfer.settings import EMAIL_USER
class Util:
    
    @staticmethod
    def send_email(data: Any) -> None:
        email_body = render_to_string(
            "password_reset.html", {"body": data.get("body")}
        )
        send_mail(
            "Reset Password",
            email_body,
            EMAIL_USER,
            [data.get("recipient")],
            fail_silently=False,
        )