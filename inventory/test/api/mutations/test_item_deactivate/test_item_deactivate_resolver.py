from typing import List

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase

from inventory.api.mutations.item_deactivate.item_deactivate_input import ItemDeactivateInput
from inventory.api.mutations.item_deactivate.item_deactivate_payload import ItemDeactivatePayload
from inventory.api.mutations.item_deactivate.item_deactivate_resolver import item_deactivate_resolver
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node


class ItemDeactivateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1)
        self.item = temp[0]

    async def test_item_deactivate_resolver_response(self):
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemDeactivateInput(id=id_node)
        result: ItemDeactivatePayload = await item_deactivate_resolver(item_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemDeactivatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if item is the same that input
        self.assertEqual(result.node.id, id_node)

        # Test if item is not is_active
        self.assertFalse(result.node.is_active)

    async def test_item_deactivate_resolver_side_effect(self):
        # Building input
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemDeactivateInput(id=id_node)

        # Updating is_active
        await item_deactivate_resolver(item_input)

        # Checking if field was updated in database
        item = await Item.objects.aget(pk=self.item.id)
        self.assertFalse(item.is_active)
