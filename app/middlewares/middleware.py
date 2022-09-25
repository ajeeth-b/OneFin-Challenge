from .models import RequestLog


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        RequestLog(path=request.get_full_path()).save()
        response = self.get_response(request)
        return response
