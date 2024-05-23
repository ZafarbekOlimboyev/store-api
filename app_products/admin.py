from django.contrib import admin

from .models import ProImageModel, CategoriesModel, ProductsModel

admin.site.register(ProductsModel)
admin.site.register(ProImageModel)
admin.site.register(CategoriesModel)
