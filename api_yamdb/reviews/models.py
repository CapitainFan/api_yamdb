from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField("Название", max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField("Название", max_length=256)
    description = models.TextField("Описание", null=True, blank=True)
    year = models.IntegerField('Год выпуска')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        db_column="category",
        verbose_name="Категория",
        related_name="title", null=True, blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        verbose_name='Жанр'
    )

    def __str__(self):
        return self.name
