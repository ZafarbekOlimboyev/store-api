import datetime
import logging

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from config.permissions import Cheak, IsAdminOrReadOnly, IsSuperUserOrAdminUser
from .models import CategoriesModel, ProductsModel, ProImageModel
from .paginations import StandardResultsSetPagination
from .serializers import ProductsSerializer, CategoriesSerializer
from .filters import ProductsFilterSet

logger = logging.getLogger(__name__)


class CategoryViewSet(ModelViewSet):
    queryset = CategoriesModel.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    @swagger_auto_schema(tags=['Category'])
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

    @swagger_auto_schema(tags=['Category'])
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

    @swagger_auto_schema(tags=['Category'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(tags=['Category'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Category'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Category'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ProductsViewSet(ModelViewSet):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [Cheak, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilterSet
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(tags=['Products'])
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

    @swagger_auto_schema(tags=['Products'])
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

    @swagger_auto_schema(tags=['Products'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(self, request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Products'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class GetProductView(ListAPIView):
    queryset = ProductsModel.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(tags=['Category'])
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


@swagger_auto_schema(tags=['Category'], method='patch')
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


class ImageView(APIView):
    http_method_names = ['post', 'put']

    @swagger_auto_schema(tags=['Update Product Images'])
    def put(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        images = request.FILES.getlist('images')

        if not product_id or not images:
            return Response({'error': 'product_id and images are required'}, status=status.HTTP_400_BAD_REQUEST)

        if not ProductsModel.objects.filter(id=product_id).exists():
            return Response({'error': f"Product with id {product_id} does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            ProImageModel.objects.filter(product_id=product_id).delete()
            new_images = [ProImageModel(image=image, product_id=product_id) for image in images]
        except:
            raise ValueError(f"Product with id {product_id} does not exist")

        try:
            ProImageModel.objects.bulk_create(new_images)

            return Response({'message': 'New images added successfully'}, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'International Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(tags=['Update Product Images'])
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        images = request.FILES.getlist('images')

        if not product_id or not images:
            return Response({'error': 'product_id and images are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_images = [ProImageModel(image=image, product_id=product_id) for image in images]
            ProImageModel.objects.bulk_create(new_images)

            return Response({'message': 'Images updated successfully'}, status=status.HTTP_200_OK)
        except:
            return Response(data={'message': 'International Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
