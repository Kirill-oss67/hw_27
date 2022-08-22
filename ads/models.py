from django.db import models


class Ad(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=100)


class User(models.Model):
    pass


class Location(models.Model):
    pass