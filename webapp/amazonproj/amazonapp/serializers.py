from .models import *
from rest_framework import serializers

"""This is for the API to be consumed by React.
"""

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'reviewer_id', 'review_text', 'star_rating', 'review_time')


class ProductQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuality
        fields = ('id', 'name')


class ProductQualityScoreSerializer(serializers.ModelSerializer):
    product_quality = ProductQualitySerializer(read_only=True)

    class Meta:
        model = ProductQualityScore
        fields = ('id', 'score', 'product_quality')


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    review_set = ReviewSerializer(many=True, read_only=True)
    productqualityscore_set = ProductQualityScoreSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'categories', 'review_set', 'productqualityscore_set', 'image_url')
