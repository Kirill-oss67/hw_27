from django.http import HttpResponse
from django.shortcuts import render


def my_func(request):
    return HttpResponse({"status": "ok"}, 200)
