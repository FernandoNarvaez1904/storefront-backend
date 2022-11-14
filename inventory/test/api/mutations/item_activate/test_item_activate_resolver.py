from typing import List

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase

from inventory.api.mutations.item_activate.item_activate_input import ItemActivateInput
from inventory.api.mutations.item_activate.item_activate_payload import ItemActivatePayload
from inventory.api.mutations.item_activate.item_activate_resolver import item_activate_resolver
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node


class ItemActivateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1, False)
        self.item = temp[0]

    async def test_item_activate_resolver_response(self):
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemActivateInput(id=id_node)
        result: ItemActivatePayload = await item_activate_resolver(item_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemActivatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if item is the same that input
        self.assertEqual(result.node.id, id_node)

        # Test if item is not is_active
        self.assertTrue(result.node.is_active)

    async def test_item_activate_resolver_side_effect(self):
        # Building input
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemActivateInput(id=id_node)

        # Updating is_active
        await item_activate_resolver(item_input)

        # Checking if field was updated in database
        item = await Item.objects.aget(pk=self.item.id)
        self.assertTrue(item.is_active)
