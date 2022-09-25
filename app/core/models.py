import collections
from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.


class Collection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField()
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Genere(models.Model):
    genere = models.CharField(unique=True, max_length=255)

    @staticmethod
    def parse_and_return_valid_genere(generes: str):
        valid_generes = []
        for i in generes.split(","):
            genere = i.strip().title()
            if genere:
                valid_generes.append(genere)
        return valid_generes


class Movies(models.Model):

    title = models.TextField()
    uuid = models.UUIDField()
    description = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    genere = models.ManyToManyField(Genere)
    is_active = models.BooleanField(default=True)

    @classmethod
    def create_movie_with_genere(cls, title, uuid, description, collection, generes):
        obj = cls(
            title=title,
            uuid=uuid,
            description=description,
            collection=collection,
        )
        obj.save()
        for i in generes:
            genere, _ = Genere.objects.get_or_create(genere=i)
            obj.genere.add(genere)

        return obj
