from typing import List

from django.test import TestCase

from inventory.api.mutations.item_activate.item_activate_errors import CannotActivateAlreadyActiveItem, \
    CannotActivateNonExistentItem
from inventory.api.mutations.item_activate.item_activate_input import ItemActivateInput
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import UserError


class ItemActivateInputTest(TestCase):

    async def test_validate_and_get_errors_not_existing_id(self) -> None:
        # Test not existing id
        not_existing_item_type = ItemActivateInput(id=Node.encode_id(type_name='ItemType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], CannotActivateNonExistentItem)

    async def test_validate_and_get_errors_active_item(self) -> None:
        # Test already activate item
        item = await create_bulk_of_item(1)
        inactive_item_type = ItemActivateInput(
            id=Node.encode_id(type_name='ItemType', node_id=f"{item[0].id}"))
        expected_is_not_active_error: List[UserError] = await inactive_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], CannotActivateAlreadyActiveItem)

    async def test_validate_and_get_errors_no_errors(self) -> None:
        # Test no errors
        inactive_item = await create_bulk_of_item(1, active=False, seed="not")
        item_type = ItemActivateInput(id=Node.encode_id(type_name='ItemType', node_id=f"{inactive_item[0].id}"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
