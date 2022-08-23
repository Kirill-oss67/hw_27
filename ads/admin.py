from django.contrib import admin

# Register your models here.
from ads.models import Ad, Category, User, Location


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "price", "is_published",)
    search_fields = ("name", "description",)
    list_filter = ("is_published",)


@admin.register(Category)
class AdAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username",)
    search_fields = ("username",)
    list_filter = ("role",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass