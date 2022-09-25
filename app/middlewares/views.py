from rest_framework import response, status, decorators
from rest_framework.permissions import IsAuthenticated
from .models import RequestLog


@decorators.api_view(["GET"])
@decorators.permission_classes([IsAuthenticated])
def get_request_count(request):
    count = RequestLog.objects.filter(include_for_count=True).count()
    return response.Response({"requests": count}, status=status.HTTP_200_OK)


@decorators.api_view(["POST"])
@decorators.permission_classes([IsAuthenticated])
def reset_request_count(request):
    RequestLog.objects.update(include_for_count=False)
    return response.Response(
        {"message": "request count reset successfully"},
        status=status.HTTP_200_OK,
    )
