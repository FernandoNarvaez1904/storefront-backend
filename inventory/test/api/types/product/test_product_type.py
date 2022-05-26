from django.test import TestCase

from inventory.api.types.product import ProductType
from inventory.models import Product, ProductDetail, ModifyStockDocument


class ProductTypeTest(TestCase):

    def setUp(self):
        product = Product.objects.create(
            sku="45",
        )
        ProductDetail.objects.create(
            name="ProductDetail1",
            barcode="890432",
            cost=10,
            markup=50,
            root_product=product,
            is_service=False
        )
        self.product = product

    def test_name_field(self):
        name = ProductType.name(self.product)
        self.assertEqual(self.product.current_detail.name, name)

    def test_barcode_field(self):
        barcode = ProductType.barcode(self.product)
        self.assertEqual(self.product.current_detail.barcode, barcode)

    def test_cost_field(self):
        cost = ProductType.cost(self.product)
        self.assertEqual(self.product.current_detail.cost, cost)

    def test_markup_field(self):
        markup = ProductType.markup(self.product)
        self.assertEqual(self.product.current_detail.markup, markup)

    def test_last_modified_date_field(self):
        date = ProductType.last_modified_date(self.product)
        self.assertEqual(self.product.current_detail.date, date)

    def test_current_stock(self):
        # Test for 0, no modification
        self.assertEqual(0, ProductType.current_stock(self.product))

        # Test Adding Positive
        ModifyStockDocument.objects.create(product_id=self.product, quantity_modified=5)
        self.assertEqual(5, ProductType.current_stock(self.product))

        # Test going negative from positive
        ModifyStockDocument.objects.create(product_id=self.product, quantity_modified=-20)
        self.assertEqual(-15, ProductType.current_stock(self.product))

        # Test subtracting when negative
        ModifyStockDocument.objects.create(product_id=self.product, quantity_modified=-5)
        self.assertEqual(-20, ProductType.current_stock(self.product))

        # Test going positive from negative
        ModifyStockDocument.objects.create(product_id=self.product, quantity_modified=50)
        self.assertEqual(30, ProductType.current_stock(self.product))
