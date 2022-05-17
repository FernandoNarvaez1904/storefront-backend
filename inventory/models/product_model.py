from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    is_service = models.BooleanField(default=False)
    current_detail = models.ForeignKey("ProductDetail", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)


class ProductDetail(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=48)
    cost = models.FloatField()
    markup = models.FloatField()
    root_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_versions")
