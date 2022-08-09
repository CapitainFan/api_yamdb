from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField('Год выпуска', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        db_column="category",
        verbose_name="Категория",
        related_name="title", blank=True, null=True
    )
#посмотреть отдельную таблицу для связей жанра
#https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ManyToManyField.through
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        verbose_name='жанр'
    )

    def __str__(self):
        return self.name
