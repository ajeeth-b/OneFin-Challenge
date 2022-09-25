from django.db import models
from rest_framework import response, status
import functools


def db_resourse_checker(model: models.Model, masked_model_name=None):
    def check_model_data(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except model.DoesNotExist:
                return response.Response(
                    {
                        "is_success": False,
                        "message": "{resource_name} Not Found!".format(
                            resource_name=masked_model_name or model.__name__,
                        ),
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

        return wrapper_func

    return check_model_data
