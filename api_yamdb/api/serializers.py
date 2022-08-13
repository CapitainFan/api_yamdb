from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

User = get_user_model()

RESTRICTED_USERNAME = 'me'


class SignupSerializer(serializers.ModelSerializer):
    '''Сериализация данных пользователя при регистрации
        через эндпоинт auth/sighup.'''
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


class GettingTokenSerializer(serializers.ModelSerializer):
    '''Сериализация данных для получения access-токена.'''
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    confirmation_code = serializers.CharField(
        max_length=250,
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'confirmation_code', ]


class UserSerializer(serializers.ModelSerializer):
    '''Сериализация данных пользователя для эндпоинтов users/, users/me/.'''
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
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role', ]

    def validate_username(self, value):
        if value == RESTRICTED_USERNAME:
            raise serializers.ValidationError(
                f'Использовать имя {RESTRICTED_USERNAME} '
                  'в качестве username запрещено.'
                  )
        return value


class OwnerSerializer(serializers.ModelSerializer):
    '''Сериализация данных пользователя для эндпоинта users/me/.'''

    role = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'bio', 'role', ]

    def validate_username(self, value):
        if value == RESTRICTED_USERNAME:
            raise serializers.ValidationError(
                f'Использовать имя {RESTRICTED_USERNAME} '
                  'в качестве username запрещено.'
                  )
        return value
