import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, DeleteView, ListView, CreateView, UpdateView

from ads.models import Ad, User, Category
from django.conf import settings



class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related("author").order_by("-price")
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 0)
        page_obj = paginator.get_page(page_number)
        res = []
        for ad in page_obj:
            res.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.username,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None
            })

        response = {
            "items": res,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count}
        return JsonResponse(response)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ('name', 'author', 'price', 'description', 'is_published', 'category')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(name=data['name'], author=get_object_or_404(User, pk=data['author_id']),
                                   price=data['price'],
                                   description=data['description'],
                                   is_published=data['is_published'],
                                   category=get_object_or_404(Category, pk=data['category_id']))
        return JsonResponse({
            "id": new_ad.id,
            "name": new_ad.name,
            "author_id": new_ad.author_id,
            "author": new_ad.author.username,
            "price": new_ad.price,
            "description": new_ad.description,
            "is_published": new_ad.is_published,
            "category_id": new_ad.category_id,
            "image": new_ad.image.url if new_ad.image else None
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'is_published', 'image', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data.get('name')
        self.object.price = ad_data.get('price')
        self.object.description = ad_data.get('description')
        self.object.is_published = ad_data.get('is_published')
        self.object.category_id = ad_data.get('category_id')

        self.object.save()

        response = {
            'id': self.object.id,
            'author_id': self.object.author_id,
            'author': str(self.object.author),
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 4})

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

        self.object.image = request.FILES.get('image',None)
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