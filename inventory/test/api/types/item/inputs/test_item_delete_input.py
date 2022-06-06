from typing import List

from asgiref.sync import sync_to_async
from django.test import TestCase
from strawberry_django_plus.relay import GlobalID

from inventory.api.types.item import ItemNotExistError
from inventory.api.types.item.inputs.item_delete_input import ItemDeleteInput
from inventory.models import Item
from storefront_backend.api.types import UserError


class ItemDeleteInputTest(TestCase):

    async def test_validate_and_get_errors(self):
        # Test not existing id
        not_existing_item_type = ItemDeleteInput(id=GlobalID(type_name='ItemType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], ItemNotExistError)

        # Test no errors
        item = await sync_to_async(Item.objects.create)(sku="45")
        item_type = ItemDeleteInput(id=GlobalID(type_name='ItemType', node_id=f"{item.id}"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
