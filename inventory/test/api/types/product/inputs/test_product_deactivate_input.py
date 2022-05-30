from typing import List

from django.test import TestCase
from strawberry_django_plus.relay import GlobalID

from inventory.api.types.product import ProductNotExistError, ProductIsNotActiveError
from inventory.api.types.product.inputs.product_deactivate_input import ProductDeactivateInput
from inventory.models import Item
from storefront_backend.api.types import UserError


class ProductDeactivateInputTest(TestCase):
    def setUp(self):
        product = Item.objects.create(
            sku="1",
        )
        self.product = product

        inactive_product = Item.objects.create(
            sku="2",
            is_active=False
        )
        self.inactive_product = inactive_product

    async def test_validate_and_get_errors(self):
        # Test not existing id
        not_existing_product_type = ProductDeactivateInput(id=GlobalID(type_name='ProductType', node_id='3549'))
        expected_not_exist_error: List[UserError] = await not_existing_product_type.validate_and_get_errors()
        self.assertIsInstance(expected_not_exist_error[0], ProductNotExistError)

        # Test already inactivate product
        inactive_product_type = ProductDeactivateInput(
            id=GlobalID(type_name='ProductType', node_id=f"{self.inactive_product.id}"))
        expected_is_not_active_error: List[UserError] = await inactive_product_type.validate_and_get_errors()
        self.assertIsInstance(expected_is_not_active_error[0], ProductIsNotActiveError)

        # Test no errors
        product_type = ProductDeactivateInput(id=GlobalID(type_name='ProductType', node_id=f"{self.product.id}"))
        expected_no_error: List[UserError] = await product_type.validate_and_get_errors()
        self.assertFalse(len(expected_no_error))
