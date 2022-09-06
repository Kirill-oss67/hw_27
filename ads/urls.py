from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ads.views.service import my_func
from ads.views import ad as ad_view
from ads.views import category as category_view
from ads.views import users as user_view
from ads.views import locations as location_view
from ads.views import selection as selection_view

router = routers.SimpleRouter()
router.register('locations', location_view.LocationViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', my_func),
    path('cat/', category_view.CategoryListView.as_view()),
    path('cat/create/', category_view.CategoryCreateView.as_view()),
    path('cat/<int:pk>/update/', category_view.CategoryUpdateView.as_view()),
    path('cat/<int:pk>/', category_view.CategoryDetailView.as_view()),
    path('cat/<int:pk>/delete/', category_view.CategoryDeleteView.as_view()),

    path('ad/<int:pk>/', ad_view.AdDetailView.as_view()),
    path('ad/', ad_view.AdListView.as_view()),
    path('ad/create/', ad_view.AdCreateView.as_view()),
    path('ad/<int:pk>/update/', ad_view.AdUpdateView.as_view()),
    path('ad/<int:pk>/upload_image/', ad_view.AdUploadImageView.as_view()),
    path('ad/<int:pk>/delete/', ad_view.AdDeleteView.as_view()),

    path('user/', user_view.UserListView.as_view()),
    path('user/create/', user_view.UserCreateView.as_view()),
    path('user/<int:pk>/', user_view.UserDetailView.as_view()),
    path('user/<int:pk>/update/', user_view.UserUpdateView.as_view()),
    path('user/<int:pk>/delete/', user_view.UserDeleteView.as_view()),

    path('user/token/', TokenObtainPairView.as_view()),
    path('user/token/refresh/', TokenRefreshView.as_view()),

    path('selection/', selection_view.SelectionListView.as_view()),
    path('selection/<int:pk>/', selection_view.SelectionDetailView.as_view()),
    path('selection/create/', selection_view.SelectionCreateView.as_view()),
    path('selection/<int:pk>/update/', selection_view.SelectionUpdateView.as_view()),



]
urlpatterns += router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
