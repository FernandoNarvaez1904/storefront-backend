from typing import List

from asgiref.sync import async_to_sync
from django.test import TestCase

from inventory.api.mutations.item_create.item_create_errors import CannotCreateItemSkuIsNotUnique, \
    CannotCreateItemBarcodeIsNotUnique, CannotCreateItemNameIsNotUnique
from inventory.api.mutations.item_create.item_create_input import ItemCreateInput
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.types import UserError


class ItemCreateInputTest(TestCase):
    def setUp(self):
        items = async_to_sync(create_bulk_of_item)(1)
        self.item = items[0]

    async def test_validate_and_get_errors(self):
        default_args = {
            'is_service': False,
            'cost': 0.00,
            'markup': 0.00
        }
        # Test sku error
        sku_error_item_type = ItemCreateInput(sku=self.item.sku, barcode="hello", name="itemName", **default_args)
        expected_sku_error: List[UserError] = await sku_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_sku_error[0], CannotCreateItemSkuIsNotUnique)

        # Test barcode error
        barcode_error_item_type = ItemCreateInput(sku="10", barcode=self.item.barcode, name="itemName", **default_args)
        expected_barcode_error: List[UserError] = await barcode_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_barcode_error[0], CannotCreateItemBarcodeIsNotUnique)

        # Test name error
        name_error_item_type = ItemCreateInput(sku="10", barcode="someCode", name=self.item.name, **default_args)
        expected_name_error: List[UserError] = await name_error_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_name_error[0], CannotCreateItemNameIsNotUnique)

        # Test sku, barcode and nae error
        errors_item_type = ItemCreateInput(name=f"{self.item.name}", sku=f"{self.item.sku}",
                                           barcode=f"{self.item.barcode}",
                                           **default_args)
        expected_errors: List[UserError] = await errors_item_type.validate_and_get_errors()
        self.assertIsInstance(expected_errors[0], CannotCreateItemSkuIsNotUnique)
        self.assertIsInstance(expected_errors[1], CannotCreateItemBarcodeIsNotUnique)
        self.assertIsInstance(expected_errors[2], CannotCreateItemNameIsNotUnique)

        # Test should have no problem
        passing_item_type = ItemCreateInput(sku=f"{self.item.sku}1", barcode=f"{self.item.barcode}1",
                                            name=f"{self.item.name}@", **default_args)
        expected_no_error: List[UserError] = await passing_item_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
