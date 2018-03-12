from django.shortcuts import render

# http://www.django-rest-framework.org/tutorial/quickstart/
from .models import *
from rest_framework import viewsets
from .serializers import ProductSerializer


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('title')
    serializer_class = ProductSerializer
