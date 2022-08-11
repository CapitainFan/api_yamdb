import uuid
from random import choice
from string import ascii_uppercase

from django.core.mail import EmailMessage

from django.shortcuts import get_object_or_404

from users.models import User

from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken



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

# May be better to create a class for 3 function below?
def code_create_or_update(username, email):
    user = get_object_or_404(User, username=username)
    user.confirmation_code = code_generation()
    user.save()
    send_email(email)


def code_generation():
    #return str(uuid.uuid4())
    return (''.join(choice(ascii_uppercase) for i in range(12)))

def send_email(email):
    email = EmailMessage(
        body=code_generation(),
        to=[email, ]
    )
    email.send(fail_silently=False)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
