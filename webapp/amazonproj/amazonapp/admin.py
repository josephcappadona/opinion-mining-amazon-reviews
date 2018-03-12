from django.contrib import admin

from amazonapp.models import *


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(ProductQuality)
admin.site.register(ProductQualityScore)
admin.site.register(ProductQualitySnippet)
