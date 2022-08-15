from django.urls import path

from ads.views import CategoryView, my_func, AdView, AdDetailView, CategoryDetailView

urlpatterns = [
    path('', my_func),
    path('cat/', CategoryView.as_view()),
    path('ad/', AdView.as_view()),
    path('ad/int:<pk>', AdDetailView.as_view()),
    path('cat/int:<pk>', CategoryDetailView.as_view())
]
