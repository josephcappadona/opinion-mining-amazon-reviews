from django.db import models


class Product(models.Model):
    # ASIN
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=1000)
