from rest_framework import serializers
from .models import Collection, Movies


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            "id",
            "title",
            "description",
            "creator",
        )


class MovieSerializer(serializers.ModelSerializer):
    generes = serializers.SerializerMethodField()

    def get_generes(self, obj):
        return [i.genere for i in obj.genere.all()]

    class Meta:
        model = Movies
        fields = (
            "title",
            "uuid",
            "description",
            "generes",
        )


class CollectionSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = (
            "id",
            "title",
            "description",
            "movies",
        )

    def get_movies(self, obj):
        movies = Movies.objects.filter(is_active=True, collection=obj)
        movies = MovieSerializer(movies, many=True).data
        return movies
