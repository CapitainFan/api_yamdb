# from users.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from .confirmation import code_generation, send_email

User = get_user_model()

RESTRICTED_USERNAME = 'me'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', ]
        read_only_field = ('id',)


class SignupSerializer(serializers.ModelSerializer):
    '''Сериализация данных при создании пользователя не админом'''
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', ]
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, value):
        if value == RESTRICTED_USERNAME:
            raise serializers.ValidationError(
                f'Использовать имя {RESTRICTED_USERNAME} '
                  'в качестве username запрещено.'
                  )
        return value


class SignupAdminSerializer(serializers.ModelSerializer):
    '''Сериализация данных при создании пользователя админом'''
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role', ]

    def validate_username(self, value):
        if value == RESTRICTED_USERNAME:
            raise serializers.ValidationError(
                f'Использовать имя {RESTRICTED_USERNAME} '
                  'в качестве username запрещено.'
                  )
        return value

