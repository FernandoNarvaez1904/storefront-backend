from typing import List

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase

from inventory.api.mutations.item_update.Item_update_resolver import item_update_resolver
from inventory.api.mutations.item_update.item_update_input import ItemUpdateInput, ItemUpdateDataInput
from inventory.api.mutations.item_update.item_update_payload import ItemUpdatePayload
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node


class ItemUpdateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1)
        self.item = temp[0]
        self.new_data = {
            "name": "new_name",
            "cost": 10.50
        }

    async def test_item_update_resolver_response(self):
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        update_data = ItemUpdateDataInput(**self.new_data)
        item_update_input = ItemUpdateInput(id=id_node, data=update_data)

        result: ItemUpdatePayload = await item_update_resolver(item_update_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemUpdatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if item is the same that input
        self.assertEqual(result.node.id, id_node)

        # test if data was updated according to update_data
        for key, value in self.new_data.items():
            self.assertEqual(value, result.node.__getattribute__(key))

    async def test_item_update_resolver_side_effect(self):
        # Building input
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        update_data = ItemUpdateDataInput(**self.new_data)
        item_update_input = ItemUpdateInput(id=id_node, data=update_data)

        # Updating is_active
        await item_update_resolver(item_update_input)

        # test if data was updated according to update_data
        item = await Item.objects.aget(pk=self.item.id)
        for key, value in self.new_data.items():
            self.assertEqual(value, item.__getattribute__(key))
