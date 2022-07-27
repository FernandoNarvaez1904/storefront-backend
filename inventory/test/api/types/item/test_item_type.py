from asgiref.sync import async_to_sync, sync_to_async
from django.test import TestCase
from strawberry_django_plus.relay import GlobalID

from inventory.api.types.item import ItemType
from inventory.models import ItemDetail
from inventory.test.api.utils import create_bulk_of_item


class ItemTypeTest(TestCase):

    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

    async def test_name_field(self):
        name = await ItemType.name(self.item)
        self.assertEqual(self.item.current_detail.name, name)

    async def test_barcode_field(self):
        barcode = await ItemType.barcode(self.item)
        self.assertEqual(self.item.current_detail.barcode, barcode)

    async def test_cost_gql(self):
        cost = await ItemType.cost(self.item)
        self.assertEqual(self.item.current_detail.cost, cost)

    async def test_markup_gql(self):
        markup = await ItemType.markup(self.item)
        self.assertEqual(self.item.current_detail.markup, markup)

    async def test_creation_date_gql(self):
        date = await ItemType.creation_date(self.item)
        self.assertEqual(self.item.current_detail.date, date)

    async def test_price_gql(self):
        item = self.item
        price = await ItemType.price(item)
        self.assertEqual(15, price)

    async def test_version_id(self):
        id: GlobalID = await ItemType.version_id(self.item)
        self.assertEqual(f"{self.item.current_detail.id}", f"{id.node_id}")

    async def test_item_versions(self):
        # Creating a new ItemVersion
        await sync_to_async(ItemDetail.objects.create)(
            name="itemDetail2",
            barcode="89043",
            cost=10,
            markup=50,
            root_item=self.item,
        )

        list_coroutine = sync_to_async(list)
        # It is callable but pycharm does not know it
        # noinspection PyCallingNonCallable
        temp = await list_coroutine(ItemType.item_versions(root=self.item))
        item_type_result_1 = set(temp)
        filtered = await list_coroutine(ItemDetail.objects.filter(root_item=self.item))
        expected_result = set(filtered)
        self.assertEqual(item_type_result_1, expected_result)
