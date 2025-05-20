from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    favorites = models.ManyToManyField('products.Product', related_name='favorited_by', blank=True)

