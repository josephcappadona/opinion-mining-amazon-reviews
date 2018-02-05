from django.db import models
from . import Product, Category, ProductQuality, Review


class ProductQualitySnippet(models.Model):
    product = models.ForeignKey(Product, max_length=255, on_delete=models.CASCADE)
    product_quality = models.ForeignKey(ProductQuality, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    sentence = models.TextField()
