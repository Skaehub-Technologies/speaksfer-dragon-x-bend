from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from speaksfer.settings import EMAIL_USER

User = get_user_model()


def send_email(template: str, email_data: Any) -> None:
    email_body = render_to_string(template, {"body": email_data.get("body")})

    send_mail(
        email_data.get("subject"),
        email_body,
        EMAIL_USER,
        [email_data.get("recipient")],
        fail_silently=False,
    )


def generate_reset_token(email: str) -> Any:
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        encoded_pk = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        return (user, encoded_pk, token)
    return None


def create_reset_email(
    request: Any, user: Any, encoded_pk: str, token: str
) -> dict:
    current_site = get_current_site(request).domain
    reset_url = reverse(
        "verify-password-reset",
        kwargs={"encoded_pk": encoded_pk, "token": token},
    )
    absurl = f"http://{current_site}{reset_url}"
    body = {"user": user, "link": absurl}
    data = {
        "subject": "YOUR PASSWORD RESET LINK",
        "body": body,
        "recipient": user.email,
    }
    return data
