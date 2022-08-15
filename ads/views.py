from django.http import JsonResponse
from django.shortcuts import render


def my_func(request):
    return JsonResponse({"status": "ok"})
