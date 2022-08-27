from typing import List

from asgiref.sync import async_to_sync
from django.test import TestCase

from inventory.api.types.item.inputs import ItemCreateInput
from inventory.api.types.item.user_error_types import SKUNotUniqueError, BarcodeNotUniqueError
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.types import UserError


class ItemCreateInputTest(TestCase):
    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

    async def test_validate_and_get_errors(self):
        # Test sku error
        sku_error_item_type = ItemCreateInput(sku=self.item.sku, barcode="hello")
        expected_sku_error: List[UserError] = await sku_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_sku_error[0], SKUNotUniqueError)

        # Test barcode error
        barcode_error_item_type = ItemCreateInput(sku="10", barcode=self.item.barcode)
        expected_barcode_error: List[UserError] = await barcode_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_barcode_error[0], BarcodeNotUniqueError)

        # Test sku and barcode error
        errors_item_type = ItemCreateInput(sku=f"{self.item.sku}", barcode=f"{self.item.barcode}")
        expected_errors: List[UserError] = await errors_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_errors[0], SKUNotUniqueError)
        self.assertIsInstance(expected_errors[1], BarcodeNotUniqueError)

        # Test should have no problem
        passing_item_type = ItemCreateInput(sku=f"{self.item.sku}1", barcode=f"{self.item.barcode}1")
        expected_no_error: List[UserError] = await passing_item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
