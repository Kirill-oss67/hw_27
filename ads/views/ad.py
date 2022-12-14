import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, CreateView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Ad, User, Category
from ads.permissions import AdUpdateDeletePermission

from ads.serializers import AdSerializer, AdCreateSerializer


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat', [])
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)
        text = request.GET.get('name')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)
        location = request.GET.get('location')
        if text:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=int(price_from))
        if price_to:
            self.queryset = self.queryset.filter(price__lte=int(price_to))
        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer

#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdCreateView(CreateView):
#     model = Ad
#     fields = ('name', 'author', 'price', 'description', 'is_published', 'category')
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#
#         if data["is_published"] is True:
#             return JsonResponse({"error": "bad status"}, status=400)
#
#         new_ad = Ad.objects.create(name=data['name'], author=get_object_or_404(User, pk=data['author_id']),
#                                    price=data['price'],
#                                    description=data['description'],
#                                    is_published=data['is_published'],
#                                    category=get_object_or_404(Category, pk=data['category_id']))
#         return JsonResponse({
#             "id": new_ad.id,
#             "name": new_ad.name,
#             "author_id": new_ad.author_id,
#             "author": new_ad.author.username,
#             "price": new_ad.price,
#             "description": new_ad.description,
#             "is_published": new_ad.is_published,
#             "category_id": new_ad.category_id,
#             "image": new_ad.image.url if new_ad.image else None
#         })


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated, AdUpdateDeletePermission]
    serializer_class = AdSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get('image', None)
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None
        })
