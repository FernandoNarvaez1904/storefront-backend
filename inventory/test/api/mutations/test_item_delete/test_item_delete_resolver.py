from typing import List

from asgiref.sync import async_to_sync, sync_to_async
from django.test import TransactionTestCase

from inventory.api.mutations.item_delete.item_delete_input import ItemDeleteInput
from inventory.api.mutations.item_delete.item_delete_payload import ItemDeletePayload
from inventory.api.mutations.item_delete.item_delete_resolver import item_delete_resolver
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node


class ItemDeleteResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1)
        self.item = temp[0]

    async def test_item_delete_resolver_response(self):
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemDeleteInput(id=id_node)
        result: ItemDeletePayload = await item_delete_resolver(item_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemDeletePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if item is the same that input
        self.assertEqual(result.node.id, id_node)

    async def test_item_delete_resolver_side_effect(self):
        # Building input
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemDeleteInput(id=id_node)

        # Updating is_active
        await item_delete_resolver(item_input)

        # Checking if item was deleted
        item = await sync_to_async(list)(Item.objects.filter(pk=self.item.id))
        self.assertFalse(item)
