from django.db import models
from . import Product, Category, ProductQuality


class ProductQualityScoreData(models.Model):
    # id of the Amazon product (ASIN)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quality = models.ForeignKey(ProductQuality, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # pq_scores: JSON mapping “{ pq_id1: 0.7, pq_id2: 0.4, … }”
    pq_scores = models.TextField()

    def get_data(self):
        """
        Returns dict of mapping from product quality to score
        """
        pq_dict = json.loads(pq_scores)
        # TODO(ryin): fix N+1 query
        return {
            Product.objects.filter(id=pq_id): score
            for pq_id, score in pq_dict.items()
        }
