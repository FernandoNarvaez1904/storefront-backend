from typing import List

from asgiref.sync import sync_to_async
from django.test import TestCase
from graphql import ExecutionResult
from strawberry import Schema
from strawberry_django_plus.relay import GlobalID

from inventory.api.mutation import Mutation
from inventory.api.query import Query
from inventory.api.types.product import not_in_schema_types
from inventory.models import Product


class InventoryMutationTest(TestCase):
    def setUp(self):
        self.schema = Schema(query=Query, mutation=Mutation, types=not_in_schema_types)

    def test_can_introspect(self):
        self.assertIn("__schema", self.schema.introspect())

    async def test_product_create(self):
        mutation_input = """
            {
                sku:"1"
                isService:false,
                name:"Prod",
                barcode:"890432",
                cost:4.5
                markup:10
            }
        """
        product_fragment = """
            id
            sku
            isService
            isActive
            barcode
            name
            markup
            lastModifiedDate
            currentStock
            cost
            price
            __typename
        """
        user_errors_fragment = """
            field
            message
        """
        mutation_query = f"""
            mutation productCreate{{
                productCreate(input:{mutation_input}){{
                    userErrors{{
                        {user_errors_fragment}
                    }}
                    product{{
                        {product_fragment}
                    }}
                }}
            }}
        """

        product_create_execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        # Test has no execution errors
        self.assertIsNone(product_create_execution_result.errors)

        # Test data is not null
        exec_result_data: dict = product_create_execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        product_create_mutation_result: dict = exec_result_data.get("productCreate")
        self.assertIsNotNone(product_create_mutation_result)

        # Test if UserError is returned
        user_errors: List = product_create_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if product is returned
        product: dict = product_create_mutation_result.get("product")
        self.assertIsNotNone(product)

        # Test if all fields return
        self.assertNotIn(None, product.values())

        # Test if product was actually created
        pr_query_set = await sync_to_async(list)(Product.objects.filter(sku=product.get("sku")))
        self.assertTrue(pr_query_set)

    async def test_product_deactivate(self):
        product = await sync_to_async(Product.objects.create)(
            sku="1",
        )
        product_global_id = GlobalID(type_name='ProductType', node_id=f"{product.id}")
        mutation_query = f"""
            mutation deactivateProduct{{
                productDeactivate(input:{{id:"{product_global_id}"}}){{
                    userErrors{{
                        field
                        message
                    }}
                    deactivatedProduct{{
                        id
                        sku
                        isActive
                    }}
                }}
            }}
        """

        execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        # Test has no execution error
        self.assertIsNone(execution_result.errors)

        # Test data is not null
        exec_result_data: dict = execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        product_deactivate_mutation_result: dict = exec_result_data.get("productDeactivate")
        self.assertIsNotNone(product_deactivate_mutation_result)

        # Test if UserError is returned
        user_errors: List = product_deactivate_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if product is returned
        product_type_result: dict = product_deactivate_mutation_result.get("deactivatedProduct")
        self.assertIsNotNone(product_type_result)

        # Test if all fields return
        self.assertNotIn(None, product_type_result.values())

        # Test if product was changed
        product_changed: Product = await sync_to_async(Product.objects.get)(id=product_global_id.node_id)
        self.assertFalse(product_changed.is_active)

    async def test_product_activate(self):
        product = await sync_to_async(Product.objects.create)(
            sku="1",
            is_active=False
        )
        product_global_id = GlobalID(type_name='ProductType', node_id=f"{product.id}")
        mutation_query = f"""
            mutation activateProduct{{
                productActivate(input:{{id:"{product_global_id}"}}){{
                    userErrors{{
                        field
                        message
                    }}
                    activatedProduct{{
                        id
                        sku
                        isActive
                    }}
                }}
            }}
        """

        execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        # Test has no execution error
        self.assertIsNone(execution_result.errors)

        # Test data is not null
        exec_result_data: dict = execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        product_deactivate_mutation_result: dict = exec_result_data.get("productActivate")
        self.assertIsNotNone(product_deactivate_mutation_result)

        # Test if UserError is returned
        user_errors: List = product_deactivate_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if product is returned
        product_type_result: dict = product_deactivate_mutation_result.get("activatedProduct")
        self.assertIsNotNone(product_type_result)

        # Test if all fields return
        self.assertNotIn(None, product_type_result.values())

        # Test if product was changed
        product_changed: Product = await sync_to_async(Product.objects.get)(id=product_global_id.node_id)
        self.assertTrue(product_changed.is_active)
