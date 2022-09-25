from django.urls import path
from . import views

urlpatterns = [
    path("request-count/", views.get_request_count),
    path("request-count/reset/", views.reset_request_count),
]
