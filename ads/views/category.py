import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, DeleteView, ListView, UpdateView
from rest_framework.generics import CreateAPIView

from ads.models import Category
from ads.serializers import CategoryCreateSerializer


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")
        res = [{'id': cat.id, "name": cat.name} for cat in self.object_list]
        return JsonResponse(res, safe=False, json_dumps_params={"ensure_ascii": False})


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data.get('name')

        self.object.save()

        response = {
            'id': self.object.id,
            'name': self.object.name,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            return JsonResponse({"id": category.id, "name": category.name}, safe=False,
                                json_dumps_params={"ensure_ascii": False})
        except Exception as error:
            return JsonResponse({"error": error}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
