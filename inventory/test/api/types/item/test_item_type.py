from asgiref.sync import async_to_sync
from django.test import TestCase

from inventory.api.types.item import ItemType
from inventory.test.api.utils import create_bulk_of_item


class ItemTypeTest(TestCase):

    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

    def test_price_gql(self):
        # Positive Markup
        price = ItemType.price(self.item)
        self.assertEqual(15, price)

        # Negative Markup
        self.item.markup = -50
        price = ItemType.price(self.item)
        self.assertEqual(5, price)
