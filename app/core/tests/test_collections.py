from core import views
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class CollectionsListTests(SimpleTestCase):
    def test_resolve_collections(self):
        url = reverse("collections")
        self.assertEquals(resolve(url).func.view_class, views.CollectionsListAPI)


class CollectionsListAPITestGetRequest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            username="test_admin",
            password="test_admin123",
        )
        self.client.login(username=self.test_user.username, password="test_user2393")

        refresh = RefreshToken.for_user(self.test_user)
        self.refresh_token = refresh
        self.access_token = refresh.access_token
        self.AUTH_HEADER = {"HTTP_AUTHORIZATION": "Bearer {}".format(self.access_token)}

    def test_unauthorized_request_to_get_collections(self):
        response = self.client.get(
            reverse("collections"),
            content_type="application/json",
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_collections(self):
        response = self.client.get(
            reverse("collections"),
            content_type="application/json",
            **self.AUTH_HEADER,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_collections_data(self):
        response = self.client.get(
            reverse("collections"),
            content_type="application/json",
            **self.AUTH_HEADER,
        )
        response_data = response.json()
        assert "is_success" in response_data
        assert "data" in response_data


class CollectionsListAPITestPostRequest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            username="test_admin",
            password="test_admin123",
        )
        self.client.login(username=self.test_user.username, password="test_user2393")

        refresh = RefreshToken.for_user(self.test_user)
        self.refresh_token = refresh
        self.access_token = refresh.access_token
        self.AUTH_HEADER = {"HTTP_AUTHORIZATION": "Bearer {}".format(self.access_token)}

    def test_unauthorized_request_to_get_collections(self):
        response = self.client.post(
            reverse("collections"),
            content_type="application/json",
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collections_with_correct_data(self):
        post_data = {
            "title": "collection 2",
            "description": "<Description of the collection>",
            "movies": [
                {
                    "title": "Lawnmower Man 2: Beyond Cyberspace",
                    "description": "Jobe is resuscitated by Jonathan Walker. He wants Jobe to create a special computer chip that would connect all the computers in the world into one network, which Walker would control and use. But what Walker doesn't realize is a group of teenage hackers are on to him and out to stop his plan.",
                    "genres": "Action,Science Fiction",
                    "uuid": "662baa7e-e8d5-414c-9903-71e8a19c7195",
                },
                {
                    "title": "Bio-Dome",
                    "description": 'Bud and Doyle are two losers who are doing nothing with their lives. Both of their girlfriends are actively involved in saving the environment, but the two friends couldn\'t care less about saving the Earth. One day, when a group of scientists begin a mission to live inside a "Bio-Dome" for a year without outside contact, Bud and Doyle mistakenly become part of the project themselves.',
                    "genres": "Comedy",
                    "uuid": "91c69c21-1cb5-45a4-8c85-756e5da70c76",
                },
            ],
        }
        response = self.client.post(
            reverse("collections"),
            post_data,
            content_type="application/json",
            **self.AUTH_HEADER,
        )

        response_data = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        assert "is_success" in response_data
        assert "collection_uuid" in response_data

    def test_create_collections_with_incorrect_collection_data(self):

        # Testing Without Title
        post_data = {
            "title": "collection 2",
            "movies": [],
        }
        response = self.client.post(
            reverse("collections"),
            post_data,
            content_type="application/json",
            **self.AUTH_HEADER,
        )

        response_data = response.json()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response_data["is_success"] == False

        # Testing Without Desc
        post_data = {
            "description": "<Description of the collection>",
            "movies": [],
        }
        response = self.client.post(
            reverse("collections"),
            post_data,
            content_type="application/json",
            **self.AUTH_HEADER,
        )

        response_data = response.json()
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert response_data["is_success"] == False

