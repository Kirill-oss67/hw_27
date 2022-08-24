from django.db import models


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField(max_length=60)
    lat = models.FloatField()
    lng = models.FloatField()

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Администратор'
        MODERATOR = 'moderator', 'Модератор'
        MEMBER = 'member', 'Пользователь'

    first_name = models.CharField(max_length=70, null=True, blank=True)
    last_name = models.CharField(max_length=70, null=True, blank=True)
    username = models.CharField(unique=True, max_length=40)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=9, choices=Role.choices, default=Role.MEMBER)
    age = models.SmallIntegerField()
    location_id = models.ManyToManyField(Location)

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
