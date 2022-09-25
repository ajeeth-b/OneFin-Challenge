from rest_framework import response, status, decorators
from rest_framework.permissions import IsAuthenticated
from .utils import credy
from rest_framework.views import APIView
from . import models
from . import serializer
from django.db import transaction
from django.db.models import Count
from utils.decorators import db_resourse_checker


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def get_movies(request):
    page_no = int(request.query_params.get("page", "1"))
    max_retries = int(request.query_params.get("max_retries", "3"))
    max_retries = min(10, max_retries)
    success, data = credy.get_movies(page=page_no, max_retries=max_retries)
    if success == False:
        return response.Response(
            {
                "status": False,
                "Message": "Cannot reach the movies API. Try later.",
            },
            status=status.HTTP_424_FAILED_DEPENDENCY,
        )

    if data["next"]:
        data["next"] = request.build_absolute_uri(request.path) + "?page={page}".format(
            page=page_no + 1
        )
    if data["previous"]:
        data["previous"] = request.build_absolute_uri(
            request.path
        ) + "?page={page}".format(page=page_no - 1)
    return response.Response(data, status=status.HTTP_200_OK)


class CollectionsListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.id
        collections_query = models.Collection.objects.filter(
            is_active=True,
            creator_id=request.user.id,
        )
        generes_query = (
            models.Genere.objects.filter(
                movies__is_active=True,
                movies__collection__in=collections_query,
            )
            .values("genere")
            .annotate(
                count=Count("genere"),
            )
            .order_by("-count")
        )[:3]

        top_3_generes = [i["genere"] for i in generes_query]

        collections_data = serializer.CollectionListSerializer(
            collections_query,
            many=True,
        ).data

        response_data = {
            "is_success": True,
            "data": {
                "collections": collections_data,
                "favourite_genres": top_3_generes,
            },
        }
        return response.Response(
            response_data,
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def post(self, request):
        if (
            request.data.get("title", None) is None
            or request.data.get("description", None) is None
        ):
            return response.Response(
                {
                    "is_success": False,
                    "message": "Bad Request!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        collection = models.Collection(
            title=request.data["title"],
            description=request.data["description"],
            creator=request.user,
        )
        collection.save()

        try:
            for i in request.data.get("movies", []) or []:

                if i["genres"] and type(i["genres"]) != str:
                    raise TypeError
                movie_generes = models.Genere.parse_and_return_valid_genere(
                    i["genres"] or ""
                )

                models.Movies.create_movie_with_genere(
                    title=i["title"],
                    uuid=i["uuid"],
                    description=i["description"],
                    collection=collection,
                    generes=movie_generes,
                )
        except (TypeError, KeyError) as e:
            print(e)
            collection.delete()
            return response.Response(
                {"is_success": False, "message": "Bad Request!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response.Response(
            {
                "is_success": True,
                "collection_uuid": collection.id,
            },
            status=status.HTTP_201_CREATED,
        )


class CollectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def _get_collection(self, collection_id):
        collection = models.Collection.objects.get(id=collection_id)
        if collection.is_active == False:
            raise models.Collection.DoesNotExist
        return collection

    def _has_access(self, request, collection):
        return request.user.id == collection.creator_id

    @db_resourse_checker(models.Collection)
    def get(self, request, collection_id):
        collection = self._get_collection(collection_id)

        if self._has_access(request, collection) != True:
            return response.Response(
                {
                    "is_success": False,
                    "message": "You do not have access to this collection.!",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        response_data = serializer.CollectionSerializer(collection).data
        return response.Response(
            response_data,
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    @db_resourse_checker(models.Collection)
    def put(self, request, collection_id):
        if (
            request.data.get("title", None) is None
            or request.data.get("description", None) is None
        ):
            return response.Response(
                {
                    "is_success": False,
                    "message": "Bad Request!",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        collection = self._get_collection(collection_id)

        if self._has_access(request, collection) != True:
            return response.Response(
                {
                    "is_success": False,
                    "message": "You do not have access to this collection.!",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        collection.title = request.data["title"]
        collection.description = request.data["description"]
        collection.save()

        existing_movie_ids = list(
            models.Movies.objects.filter(
                collection=collection,
                is_active=True,
            ).values_list(
                "id",
                flat=True,
            )
        )
        try:
            for i in request.data.get("movies", []) or []:

                if i["genres"] and type(i["genres"]) != str:
                    raise TypeError
                movie_generes = models.Genere.parse_and_return_valid_genere(
                    i["genres"] or ""
                )

                models.Movies.create_movie_with_genere(
                    title=i["title"],
                    uuid=i["uuid"],
                    description=i["description"],
                    collection=collection,
                    generes=movie_generes,
                )
        except (TypeError, KeyError) as e:
            return response.Response(
                {"is_success": False, "message": "Bad Request!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        models.Movies.objects.filter(id__in=existing_movie_ids).update(is_active=False)

        return response.Response(
            {
                "is_success": True,
                "message": "Updated Successfully!",
            },
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    @db_resourse_checker(models.Collection)
    def delete(self, request, collection_id):
        collection = models.Collection.objects.get(id=collection_id)

        if self._has_access(request, collection) != True:
            return response.Response(
                {
                    "is_success": False,
                    "message": "You do not have access to this collection.!",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        collection.is_active = False
        collection.save()
        return response.Response(
            {
                "is_success": True,
                "message": "Collection Deleted Successfully!",
            },
            status=status.HTTP_200_OK,
        )
