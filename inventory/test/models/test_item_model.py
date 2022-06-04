from django.test import TestCase

from inventory.models import Item, ItemDetail


class ItemModelTest(TestCase):
    def setUp(self):
        item = Item.objects.create(sku="sku")

        self.item = item

    def test_make_new_detail_current_detail(self):
        # Test it will change if current is another None
        pr_dt_1 = ItemDetail.objects.create(
            name="itemDetail1",
            barcode="890432",
            cost=10,
            markup=50,
            root_item=self.item,
        )
        self.assertEqual(self.item.current_detail.id, pr_dt_1.id)
        # Test it will change if current is another detail
        pr_dt_2 = ItemDetail.objects.create(
            name="itemDetail1",
            barcode="890432d",
            cost=10,
            markup=50,
            root_item=self.item
        
        )
        self.assertEqual(self.item.current_detail.id, pr_dt_2.id)
