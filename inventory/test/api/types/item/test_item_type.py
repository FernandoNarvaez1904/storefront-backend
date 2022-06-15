from django.test import TestCase
from strawberry_django_plus.relay import GlobalID

from inventory.api.types.item import ItemType
from inventory.models import Item, ItemDetail


class ItemTypeTest(TestCase):

    def setUp(self):
        item = Item.objects.create(
            current_stock=9,
            is_service=False,
            sku="45",

        )
        ItemDetail.objects.create(
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

    def test_version_id(self):
        id: GlobalID = ItemType.version_id(self.item)
        self.assertEqual(f"{self.item.current_detail.id}", f"{id.node_id}")

    def test_item_versions(self):
        # Creating a new ItemVersion
        ItemDetail.objects.create(
            name="itemDetail2",
            barcode="89043",
            cost=10,
            markup=50,
            root_item=self.item,
        )
        
        item_type_result = set(ItemType.item_versions(root=self.item))
        expected_result = set(ItemDetail.objects.filter(root_item=self.item))
        self.assertEqual(item_type_result, expected_result)
