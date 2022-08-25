from typing import List

from asgiref.sync import async_to_sync
from django.test import TestCase
from strawberry_django_plus.relay import GlobalID

from inventory.api.types.item import ItemNotExistError, ItemIsNotActiveError, NameNotUniqueError, SKUNotUniqueError, BarcodeNotUniqueError
from inventory.api.types.item.inputs import ItemUpdateInput
from inventory.api.types.item.inputs.item_update_input import ItemUpdateDataInput 
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.types import UserError


class ItemUpdateInputTest(TestCase):
    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

        inactive_items = async_to_sync(create_bulk_of_item)(1, active=False, seed="not")
        self.inactive_item = inactive_items[0]

    async def test_validate_and_get_errors(self):
        # Test not existing id
        not_existing_item_type = ItemUpdateInput(id=GlobalID(type_name='ItemType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], ItemNotExistError)

        # Test already inactivate item
        inactive_item_type = ItemUpdateInput(
            id=GlobalID(type_name='ItemType', node_id=f"{self.inactive_item.id}"))
        expected_is_not_active_error: List[UserError] = await inactive_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], ItemIsNotActiveError)

        # Test name not unique error
        not_unique_name_item_type = ItemUpdateInput(
            id=GlobalID(type_name='ItemType', node_id=f"{self.item.id}"),
            data=ItemUpdateDataInput(name =self.inactive_item.current_detail.name)
        )
        expected_name_not_unique_error: List[UserError] = await not_unique_name_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_name_not_unique_error[0], NameNotUniqueError)

        #Test Barcode not unique error
        barcode_not_unique_item_type = ItemUpdateInput(
            id = GlobalID(type_name='ItemType', node_id=f"{self.item.id}"),
            data=ItemUpdateDataInput(barcode= self.inactive_item.current_detail.barcode)
        )
        expected_barcode_not_unique_item_type: List[UserError] = await barcode_not_unique_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_barcode_not_unique_item_type[0], BarcodeNotUniqueError)

        #Test SKU not unique error
        sku_not_unique_item_type = ItemUpdateInput(
            id=GlobalID(type_name='ItemType', node_id=f"{self.item.id}"),
            sku = self.inactive_item.sku
        )
        expected_sku_not_unique_error: List[UserError] = await sku_not_unique_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_sku_not_unique_error[0], SKUNotUniqueError)


        # Test no errors
        item_type = ItemUpdateInput(
            id=GlobalID(type_name='ItemType',
            node_id=f"{self.item.id}"),
            sku="newsku",
            data=ItemUpdateDataInput(name="newname", barcode="newbarcode"))
        expected_no_error: List[UserError] = await item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
