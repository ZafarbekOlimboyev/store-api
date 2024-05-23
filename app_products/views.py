import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view

from config.permissions import Cheak, IsAdminOrReadOnly
from .models import CategoriesModel, ProductsModel
from .paginations import StandardResultsSetPagination
from .serializers import ProductsSerializer, CategoriesSerializer


class CategoryViewSet(ModelViewSet):
    queryset = CategoriesModel.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = {
            "variant": "success",
            "msg": "Category is successfully created",
            "innerData": serializer.data,
            "totalCount": self.queryset.count()
        }
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        res = {
            "variant": "success",
            "msg": "All categories",
            "innerData": serializer.data,
            "totalCount": self.queryset.count()
        }
        return Response(res)


class ProductsViewSet(ModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [Cheak, ]
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = {
            "variant": "success",
            "msg": "Product is successfully created",
            "innerData": serializer.data,
            "totalCount": self.queryset.count()
        }
        return Response(res, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        res = {
            "variant": "success",
            "msg": "All products",
            "innerData": serializer.data,
            "totalCount": self.queryset.count()
        }
        return Response(serializer.data)


class GetProductView(ListAPIView):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        try:
            category = self.kwargs.get('category')
            cat = CategoriesModel.objects.get(category=category)
            queryset = self.filter_queryset(self.get_queryset().filter(category_id=cat))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response(data={
                'msg': "Category was not found"
            }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_product_view(request, pk):
    try:
        if request.user.is_staff or request.user.is_superuser:
            try:
                product = ProductsModel.objects.get(pk=pk)
            except:
                return Response(data={"msg": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            product.available = not product.available
            product.updateAt = datetime.datetime.now()
            product.save()

            serializer = ProductsSerializer(product)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response(data={"msg": f"Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


