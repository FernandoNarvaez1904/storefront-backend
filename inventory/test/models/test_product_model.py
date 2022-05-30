from django.test import TestCase

from inventory.models import Item, ItemDetail


class ProductModelTest(TestCase):
    def setUp(self):
        product = Item.objects.create(
            sku="45",
        )

        self.product = product

    def test_make_new_detail_current_detail(self):
        # Test it will change if current is another None
        pr_dt_1 = ItemDetail.objects.create(
            name="ProductDetail1",
            barcode="890432",
            cost=10,
            markup=50,
            root_product=self.product
        )
        self.assertEqual(self.product.current_detail.id, pr_dt_1.id)
        # Test it will change if current is another detail
        pr_dt_2 = ItemDetail.objects.create(
            name="ProductDetail1",
            barcode="890432",
            cost=10,
            markup=50,
            root_product=self.product
        )
        self.assertEqual(self.product.current_detail.id, pr_dt_2.id)
