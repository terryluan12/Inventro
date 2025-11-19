from django.http import HttpRequest, JsonResponse


def _json_ok(message: str) -> JsonResponse:
    return JsonResponse({"status": "ok", "message": message})


def healthz(request: HttpRequest) -> JsonResponse:
    return _json_ok("service alive")


def ready(request: HttpRequest) -> JsonResponse:
    return _json_ok("service ready")
