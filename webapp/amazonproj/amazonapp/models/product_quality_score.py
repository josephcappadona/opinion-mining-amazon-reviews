from django.db import models
from . import Product, Category, ProductQuality


class ProductQualityScore(models.Model):
    # id of the Amazon product (ASIN)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quality = models.ForeignKey(ProductQuality, on_delete=models.CASCADE)
    # score: [-1, 1]
    score = models.FloatField()

    def __str__(self):
        return '({}) {}: {}'.format(self.product.title, self.product_quality.name, self.score)
