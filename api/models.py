from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(
        max_length=10,
        unique=True
    )


class Genres(models.Model):
    name = models.CharField(max_length=10)
    slug = models.SlugField(
        max_length=10,
        unique=True
    )


class Titles(models.Model):
    name = models.CharField(max_length=90)
    year = models.IntegerField()
    description = models.TextField(
        max_length=200,
        blank=True
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='genre'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.PROTECT,
        related_name='categories'
    )
