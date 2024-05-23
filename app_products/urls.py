from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductsViewSet, CategoryViewSet, GetProductView, update_product_view

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('products', ProductsViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('get/products/category/<str:category>', GetProductView.as_view()),
    path('/update/product/available/<int:pk>', update_product_view)
]
