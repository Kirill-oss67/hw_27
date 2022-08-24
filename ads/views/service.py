from django.http import JsonResponse


def my_func(request):
    return JsonResponse({"status": "ok"})
