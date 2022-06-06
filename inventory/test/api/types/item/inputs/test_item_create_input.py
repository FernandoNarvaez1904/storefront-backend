from typing import List

from django.test import TestCase

from inventory.api.types.item.inputs import ItemCreateInput
from inventory.api.types.item.user_error_types import SKUNotUniqueError, BarcodeNotUniqueError
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError


class ItemCreateInputTest(TestCase):
    def setUp(self):
        item = Item.objects.create(sku="1")
        ItemDetail.objects.create(
            name="itemDetail1",
            barcode="barcode",
            cost=10,
            markup=50,
            root_item=item,
        )
        self.item = item

    async def test_validate_and_get_errors(self):
        # Test sku error
        sku_error_item_type = ItemCreateInput(sku="1", barcode="hello")
        expected_sku_error: List[UserError] = await sku_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_sku_error[0], SKUNotUniqueError)

        # Test barcode error
        barcode_error_item_type = ItemCreateInput(sku="10", barcode="barcode")
        expected_barcode_error: List[UserError] = await barcode_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_barcode_error[0], BarcodeNotUniqueError)

        # Test sku and barcode error
        errors_item_type = ItemCreateInput(sku="1", barcode="barcode")
        expected_errors: List[UserError] = await errors_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_errors[0], SKUNotUniqueError)
        self.assertIsInstance(expected_errors[1], BarcodeNotUniqueError)

        # Test should have no problem
        passing_item_type = ItemCreateInput(sku="some", barcode="some_code")
        expected_no_error: List[UserError] = await passing_item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
