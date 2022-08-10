import uuid

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404

from users.models import User


def code_generation():
    return str(uuid.uuid4())

def send_email(email):
    email = EmailMessage(
        body=code_generation(),
        to=[email, ]
    )
    email.send(fail_silently=False)


# def code_generation(user):
#     return default_token_generator.make_token(user)

# # Вынести отправку в отдельный класс или файл
# def send_email(username):
#     # confirmation_code = default_token_generator.make_token(user)
#     user = get_object_or_404(User, username=username)
#     confirmation_code = code_generation(user)
#     # to = user.email
#     # body = user.confirmation_code
#     print('confirmation_code')
#     email = EmailMessage(
#         body=confirmation_code,
#         to=[user.email, ]
#     )
#     email.send(fail_silently=False)