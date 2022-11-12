import datetime

from asgiref.sync import sync_to_async
from django.test import TransactionTestCase
from django.utils import timezone

from inventory.api.mutations.item_create.item_create_input import ItemCreateInput
from inventory.api.mutations.item_create.item_create_payload import ItemCreatePayload
from inventory.api.mutations.item_create.item_create_resolver import item_create_resolver
from inventory.models import Item


class ItemCreateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        self.default_data = {
            "sku": "sku",
            "is_service": False,
            "name": "name",
            "barcode": "barcode",
            "cost": 50,
            "markup": 25,
        }

    async def test_item_create_resolver_response(self):
        input_item = ItemCreateInput(**self.default_data)
        result: ItemCreatePayload = await item_create_resolver(input_item)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemCreatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if creation date is correct
        self.assertAlmostEqual(result.node.creation_date, timezone.now(),
                               delta=datetime.timedelta(seconds=0.5))

        # Test if current_stock equals 0
        self.assertEqual(result.node.current_stock, 0)

        # Test if item is_active
        self.assertTrue(result.node.is_active)

        # Test if response has all input data
        for key, value in self.default_data.items():
            self.assertEqual(value, result.node.__getattribute__(key))

    async def test_item_create_resolver_side_effect(self):
        input_item = ItemCreateInput(**self.default_data)
        await item_create_resolver(input_item)

        item_count = await Item.objects.acount()
        # Test if some item was created
        self.assertEqual(item_count, 1)

        # Test if an item with the input_data exist
        item = await sync_to_async(list)(Item.objects.filter(**self.default_data))
        # Test if item is not empty
        self.assertTrue(item)
        # Test that not duplication exist
        self.assertEqual(len(item), 1)
