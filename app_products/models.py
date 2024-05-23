from django.db import models


class CategoriesModel(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'


class ProductsModel(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    units = models.CharField(max_length=255)
    description = models.CharField(max_length=765)
    urls = models.JSONField(default=list, blank=True)
    info = models.JSONField(default=list, blank=True)
    category_id = models.ForeignKey(CategoriesModel, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now=True)
    updateAt = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'Products'


class ProImageModel(models.Model):
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%y/%m/%d/')

    def __str__(self):
        return self.image

    class Meta:
        db_table = 'product_images'
        verbose_name_plural = 'Products Images'
