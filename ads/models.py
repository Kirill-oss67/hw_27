from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField(max_length=60)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        MEMBER = 'member', 'Пользователь'
    role = models.CharField(max_length=9, choices=Role.choices, default=Role.MEMBER)
    age = models.SmallIntegerField(null=True,blank=True)
    locations = models.ManyToManyField(Location)
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']


class Ad(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

class Selection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)
    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"

    def __str__(self):
        return self.name
