from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя',
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
        verbose_name='Почтовый адрес',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Имя пользователя',
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Фамилия пользователя',
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография пользователя',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Текущая роль пользователя',
    )
    password = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Пароль'
    )
    # confirmation_code = models.CharField(
    #     blank=True,
    #     verbose_name='Код подтверждения',
    # )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    
    def __str__(self):
        """Строковое представление модели."""
        return self.username


    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True