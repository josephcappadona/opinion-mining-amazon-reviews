from django.db import models


class ProductQuality(models.Model):
    name = models.CharField(max_length=255)
