from django.db import models
from . import Category


class Product(models.Model):
    # ASIN
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=1000)
    categories = models.ManyToManyField(Category)
    price = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '{}'.format(self.title)
