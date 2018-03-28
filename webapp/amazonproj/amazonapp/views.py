from django.shortcuts import render


# http://www.django-rest-framework.org/tutorial/quickstart/
from .models import *
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ProductSerializer


# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('title')
    serializer_class = ProductSerializer

    def list(self, request):
        # filter out those that dont match the search query
        query = request.GET['q']
        if query:
            filtered_products = Product.objects.all().filter(
                title__startswith=query
            ).order_by('title')
        else:
            filtered_products = self.get_queryset()
        serializer = self.get_serializer(filtered_products, many=True)
        return Response(serializer.data)
