from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from . import Product


class Review(models.Model):
    """
    Sample review data:
    {
      "reviewerID": "A2SUAM1J3GNN3B",
      "asin": "0000013714",
      "reviewerName": "J. McDonald",
      "helpful": [2, 3],
      "reviewText": "I bought this for my husband who plays the piano.  He is having a wonderful time playing these old hymns.  The music  is at times hard to read because we think the book was published for singing from more than playing from.  Great purchase though!",
      "overall": 5.0,
      "summary": "Heavenly Highway Hymns",
      "unixReviewTime": 1252800000,
      "reviewTime": "09 13, 2009"
    }
    """
    reviewer_id = models.CharField(max_length=255)
    product = models.ForeignKey(Product, max_length=255, on_delete=models.CASCADE)
    num_helpful = models.IntegerField(default=0)
    num_unhelpful = models.IntegerField(default=0)
    review_text = models.TextField()

    # https://docs.djangoproject.com/en/dev/ref/validators/#how-validators-are-run
    star_rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    summary = models.TextField()
    review_time = models.CharField(max_length=255)
