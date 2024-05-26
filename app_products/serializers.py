from rest_framework.serializers import ModelSerializer, SerializerMethodField, ListField, FileField, Serializer

from .models import ProductsModel, CategoriesModel, ProImageModel


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = CategoriesModel
        fields = "__all__"


class ProImageSerializer(ModelSerializer):
    class Meta:
        model = ProImageModel
        fields = ['image']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(instance.image.url)
        return instance.image.url


class ProductsSerializer(ModelSerializer):
    images = ProImageSerializer(many=True, read_only=True)
    uploaded_images = ListField(
        child=FileField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    category = SerializerMethodField(method_name='get_category', read_only=True)

    class Meta:
        model = ProductsModel
        fields = [
            'id', 'title', 'price', 'units',
            'description', 'category_id', 'category',
            'info', 'uploaded_images', 'images',
            'available', 'createdAt', 'updateAt',
        ]
        extra_kwargs = {
            'available': {'read_only': True},
            'createdAt': {'read_only': True},
            'updateAt': {'read_only': True},
            'category_id': {'write_only': True}
        }

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images')
        product = ProductsModel.objects.create(**validated_data)
        for image in images:
            ProImageModel.objects.create(product=product, image=image)

        return product

    def get_category(self, obj):
        return obj.category_id.category


class UpdateImgSerializer(Serializer):
    uploaded_images = ListField(
        child=FileField(allow_empty_file=False, use_url=False),
        write_only=True
    )
