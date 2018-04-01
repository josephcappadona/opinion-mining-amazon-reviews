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
        search_query = request.GET.get('search')
        compare_query = request.GET.get('compare')
        # import code;code.interact(local=locals())
        if search_query:
            filtered_products = Product.objects.all().filter(
                title__startswith=search_query
            ).order_by('title')
        elif compare_query:
            # compare_query has a list of asins. filter by these asins!
            asins = compare_query.split(',')
            filtered_products = Product.objects.all().filter(
                pk__in=asins
            ).order_by('title')
        else:
            filtered_products = self.get_queryset()
        serializer = self.get_serializer(filtered_products, many=True)
        return Response(serializer.data)
