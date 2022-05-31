from django.test import TestCase

from inventory.api.types.item import ItemType
from inventory.models import Item, ItemDetail


class ItemTypeTest(TestCase):

    def setUp(self):
        item = Item.objects.create(
            current_stock=9,
            is_service=False

        )
        ItemDetail.objects.create(
            sku="45",
            name="itemDetail1",
            barcode="890432",
            cost=10,
            markup=50,
            root_item=item,
        )
        self.item = item

    def test_name_field(self):
        name = ItemType.name(self.item)
        self.assertEqual(self.item.current_detail.name, name)

    def test_barcode_field(self):
        barcode = ItemType.barcode(self.item)
        self.assertEqual(self.item.current_detail.barcode, barcode)

    def test_cost_field(self):
        cost = ItemType.cost(self.item)
        self.assertEqual(self.item.current_detail.cost, cost)

    def test_markup_field(self):
        markup = ItemType.markup(self.item)
        self.assertEqual(self.item.current_detail.markup, markup)

    def test_last_modified_date_field(self):
        date = ItemType.last_modified_date(self.item)
        self.assertEqual(self.item.current_detail.date, date)

    def test_price_field(self):
        # Positive Markup
        price = ItemType.price(self.item)
        self.assertEqual(15, price)

        # Negative Markup
        self.item.current_detail.markup = -50
        price = ItemType.price(self.item)
        self.assertEqual(5, price)
