from typing import List

from django.test import TestCase

from inventory.api.mutations.item_delete.item_delete_errors import CannotDeleteNonExistentItem
from inventory.api.mutations.item_delete.item_delete_input import ItemDeleteInput
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import UserError


class ItemDeleteInputTest(TestCase):

    async def test_validate_and_get_errors_no_errors(self) -> None:
        # Test no errors
        items = await create_bulk_of_item(1)
        item = items[0]
        item_type = ItemDeleteInput(id=Node.encode_id(type_name='ItemType', node_id=f"{item.id}"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))

    async def test_validate_and_get_errors_id(self) -> None:
        # Test not existing id
        not_existing_item_type = ItemDeleteInput(id=Node.encode_id(type_name='ItemType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], CannotDeleteNonExistentItem)
