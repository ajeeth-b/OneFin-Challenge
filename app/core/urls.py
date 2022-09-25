from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.get_movies),
    path("collection/", views.CollectionsListAPI.as_view()),
    path("collection/<uuid:collection_id>/", views.CollectionAPI.as_view()),
]
