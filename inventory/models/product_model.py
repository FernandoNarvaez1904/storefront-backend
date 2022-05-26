from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    current_detail = models.ForeignKey("ProductDetail", on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)


class ProductDetail(models.Model):
    is_service = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=48)
    cost = models.FloatField()
    markup = models.FloatField()
    root_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_versions")


@receiver(post_save, sender=ProductDetail)
def make_new_detail_current_detail(sender, instance: ProductDetail, **kwargs):
    root_product = instance.root_product
    root_product.current_detail = instance
    root_product.save()
