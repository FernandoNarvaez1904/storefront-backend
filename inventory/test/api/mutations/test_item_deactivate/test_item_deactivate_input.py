from typing import List

from asgiref.sync import async_to_sync
from django.test import TestCase

from inventory.api.mutations.item_deactivate.item_deactivate_errors import CannotDeactivateNonExistentItem, \
    CannotDeactivateInactiveItem
from inventory.api.mutations.item_deactivate.item_deactivate_input import ItemDeactivateInput
from inventory.api.types.item import ItemType
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.types import UserError


class ItemDeactivateInputTest(TestCase):
    def setUp(self) -> None:
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

        inactive_items = async_to_sync(create_bulk_of_item)(1, active=False, seed="not")
        self.inactive_item = inactive_items[0]

    async def test_validate_and_get_errors_not_existing_id(self) -> None:
        # Test not existing id
        not_existing_item_type = ItemDeactivateInput(id=ItemType.encode_id('3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], CannotDeactivateNonExistentItem)

    async def test_validate_and_get_errors_non_active_item(self) -> None:
        # Test already inactivate item
        inactive_item_type = ItemDeactivateInput(
            id=ItemType.encode_id(f"{self.inactive_item.id}"))
        expected_is_not_active_error: List[UserError] = await inactive_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], CannotDeactivateInactiveItem)

    async def test_validate_and_get_errors_no_errors(self) -> None:
        # Test no errors
        item_type = ItemDeactivateInput(id=ItemType.encode_id(f"{self.item.id}"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
