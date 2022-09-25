import collections
from django.db import models

# Create your models here.


class Collection(models.Model):
    title = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)


class Genere(models.Model):
    genere = models.CharField(max_length=255)


class Movies(models.Model):

    title = models.TextField()
    uuid = models.UUIDField()
    description = models.TextField()
    collections = models.ForeignKey(Collection, on_delete=models.CASCADE)
    genere = models.ManyToManyField(Genere)
    is_active = models.BooleanField(default=True)
