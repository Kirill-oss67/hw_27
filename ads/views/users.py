import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import User, Location


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.filter(ad__is_published=True).annotate(
            total_ads=Count('ad')
        ).order_by('username')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 0)
        page_obj = paginator.get_page(page_number)
        res = []
        for user in page_obj:
            res.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": list(map(str, user.locations.all())),
                "total_ads": user.total_ads
            })

        response = {
            "items": res,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count}
        return JsonResponse(response)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            # "locations": list(map(str, user.locations.all())),
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ('first_name', 'last_name', 'username', 'password', 'role', 'age', 'locations')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_user = User.objects.create(first_name=data['first_name'],
                                       last_name=data['last_name'],
                                       username=data['username'],
                                       password=data['password'],
                                       role=data['role'],
                                       age=data['age'])

        for location_name in data['locations']:
            location, created = Location.objects.get_or_create(name=location_name)
            new_user.locations.add(location)
        new_user.save()

        return JsonResponse({
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "username": new_user.username,
            "role": new_user.role,
            "age": new_user.age,
            'locations': list(map(str, new_user.locations.all()))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'username', 'password', 'role', 'age', 'locations')

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.first_name = data["first_name"]
        self.object.last_name = data["last_name"]
        self.object.username = data["username"]
        self.object.role = data['role']
        self.object.age = data['age']
        for location_name in data['locations']:
            location, created = Location.objects.get_or_create(name=location_name)
            self.object.locations.add(location)
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all()))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
