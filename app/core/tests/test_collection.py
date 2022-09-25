from core import views, models as core_models
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import uuid


class CollectionListTests(SimpleTestCase):
    def test_resolve_collection(self):
        url = reverse("collection", kwargs={"collection_id": uuid.uuid4()})
        self.assertEquals(resolve(url).func.view_class, views.CollectionAPI)


class CollectionAPITestGetRequest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.TEST_USER = User.objects.create_user(
            username="test_admin",
            password="test_admin123",
        )
        self.client.login(username=self.TEST_USER.username, password="TEST_USER2393")

        refresh = RefreshToken.for_user(self.TEST_USER)
        self.refresh_token = refresh
        self.access_token = refresh.access_token
        self.AUTH_HEADER = {"HTTP_AUTHORIZATION": "Bearer {}".format(self.access_token)}
        self.COLLECTION = core_models.Collection(
            title="title",
            description="description",
            creator=self.TEST_USER,
        )
        self.TEST_URL = reverse(
            "collection",
            kwargs={"collection_id": self.COLLECTION.id},
        )

    def test_unauthorized_request_to_get_collection(self):
        response = self.client.get(
            self.TEST_URL,
            content_type="application/json",
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_collection(self):
        response = self.client.get(
            self.TEST_URL,
            content_type="application/json",
            **self.AUTH_HEADER,
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()["collection_uuid"], self.COLLECTION.id)


# def test_get_collection_data(self):
#     response = self.client.get(
#         self.TEST_URL,
#         content_type="application/json",
#         **self.AUTH_HEADER,
#     )
#     response_data = response.json()
#     assert "is_success" in response_data
#     assert "data" in response_data
