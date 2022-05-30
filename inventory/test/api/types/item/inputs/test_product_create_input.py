from typing import List

from django.test import TestCase

from inventory.api.types.item import ProductCreateInput
from inventory.api.types.item.user_error_types import SKUNotUniqueError, BarcodeNotUniqueError
from inventory.models import Item, ItemDetail
from storefront_backend.api.types import UserError


class ProductCreateInputTest(TestCase):
    def setUp(self):
        product = Item.objects.create(
            sku="1",
        )
        ItemDetail.objects.create(
            name="ProductDetail1",
            barcode="barcode",
            cost=10,
            markup=50,
            root_product=product,
            is_service=False,
        )
        self.product = product

    async def test_validate_and_get_errors(self):
        # Test sku error
        sku_error_product_type = ProductCreateInput(sku="1", barcode="hello")
        expected_sku_error: List[UserError] = await sku_error_product_type.validate_and_get_errors()
        self.assertIsInstance(expected_sku_error[0], SKUNotUniqueError)

        # Test barcode error
        barcode_error_product_type = ProductCreateInput(sku="10", barcode="barcode")
        expected_barcode_error: List[UserError] = await barcode_error_product_type.validate_and_get_errors()
        self.assertIsInstance(expected_barcode_error[0], BarcodeNotUniqueError)

        # Test sku and barcode error
        errors_product_type = ProductCreateInput(sku="1", barcode="barcode")
        expected_errors: List[UserError] = await errors_product_type.validate_and_get_errors()
        self.assertIsInstance(expected_errors[0], SKUNotUniqueError)
        self.assertIsInstance(expected_errors[1], BarcodeNotUniqueError)

        # Test should have no problem
        passing_product_type = ProductCreateInput(sku="some", barcode="some_code")
        expected_no_error: List[UserError] = await passing_product_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))