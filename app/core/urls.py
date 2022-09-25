from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.get_movies, name="get_movies",),
    path("collection/", views.CollectionsListAPI.as_view(), name="collections",),
    path("collection/<uuid:collection_id>/", views.CollectionAPI.as_view(), name="collection",),
]
