from typing import List

from asgiref.sync import async_to_sync
from django.test import TestCase

from inventory.api.types.item import ItemNotExistError, ItemIsActiveError
from inventory.api.types.item.inputs import ItemActivateInput
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import UserError


class ItemActivateInputTest(TestCase):
    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

        inactive_items = async_to_sync(create_bulk_of_item)(1, active=False, seed="not")
        self.inactive_item = inactive_items[0]

    async def test_validate_and_get_errors(self):
        # Test not existing id
        not_existing_item_type = ItemActivateInput(id=Node.encode_id(type_name='ItemType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], ItemNotExistError)

        # Test already activate item
        inactive_item_type = ItemActivateInput(
            id=Node.encode_id(type_name='ItemType', node_id=f"{self.item.id}"))
        expected_is_not_active_error: List[UserError] = await inactive_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], ItemIsActiveError)

        # Test no errors
        item_type = ItemActivateInput(id=Node.encode_id(type_name='ItemType', node_id=f"{self.inactive_item.id}"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
