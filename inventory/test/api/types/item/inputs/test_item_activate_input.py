from typing import List

from django.test import TestCase
from strawberry_django_plus.relay import GlobalID

from inventory.api.types.item import ItemNotExistError, ItemIsActiveError
from inventory.api.types.item.inputs.item_activate_input import ItemActivateInput
from inventory.models import Item
from storefront_backend.api.types import UserError


class ItemActivateInputTest(TestCase):
    def setUp(self):
        item = Item.objects.create(sku="sku")
        self.item = item

        inactive_item = Item.objects.create(
            is_active=False
        )
        self.inactive_item = inactive_item

    async def test_validate_and_get_errors(self):
        # Test not existing id
        not_existing_item_type = ItemActivateInput(id=GlobalID(type_name='ItemType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], ItemNotExistError)

        # Test already activate item
        inactive_item_type = ItemActivateInput(
            id=GlobalID(type_name='ItemType', node_id=f"{self.item.id}"))
        expected_is_not_active_error: List[UserError] = await inactive_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], ItemIsActiveError)

        # Test no errors
        item_type = ItemActivateInput(id=GlobalID(type_name='ItemType', node_id=f"{self.inactive_item.id}"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
