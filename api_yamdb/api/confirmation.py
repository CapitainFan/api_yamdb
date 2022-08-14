from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from api_yamdb.settings import SUBJECT, SENDEREMAIL


def send_email(email, confirmation_code):
    email = EmailMessage(
        subject=SUBJECT,
        from_email=SENDEREMAIL,
        body=confirmation_code,
        to=[email, ]
    )
    email.send(fail_silently=False)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
