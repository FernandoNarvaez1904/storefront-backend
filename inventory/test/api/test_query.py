from typing import List

from asgiref.sync import sync_to_async
from django.test import TestCase
from strawberry import Schema
from strawberry.types import ExecutionResult

from inventory.api.query import Query
from inventory.models import Product, ProductDetail


async def create_bulk_of_product(num: int) -> List[Product]:
    product_list = []
    for i in range(num):
        product = await sync_to_async(Product.objects.create)(
            sku=i,
        )

        await sync_to_async(ProductDetail.objects.create)(
            is_service=False,
            name=f"ProductDetail{i}",
            barcode="890432",
            cost=10,
            markup=50,
            root_product=product
        )
        product_list.append(product)
    return product_list


class InventoryQueryTest(TestCase):
    def setUp(self):
        self.schema = Schema(query=Query)

    def test_can_introspect(self):
        self.assertIn("__schema", self.schema.introspect())

    # I tested the product_connection and product in the same test, because
    # I needed the same database objects for the global id.
    async def test_product_queries(self):
        product_node_query_fragment = """
            id
            sku
            isService
            isActive
            barcode
            cost
            currentStock
            lastModifiedDate
            markup
            name
            price
        """
        query_connection = f"""
       {{
          productConnection(
            # Args were included to test if they exist
            before: null
            after: null
            first: null
            last: null
          ){{
            edges{{
              cursor
              node{{
                {product_node_query_fragment}
              }}
            }}
            totalCount
            __typename
          }}
        }}
        """

        # Testing for empty connection
        connection_query_result: ExecutionResult = await self.schema.execute(query_connection)
        expected_empty_result = {
            'data': {'productConnection': {'edges': [], 'totalCount': 0, '__typename': 'ProductTypeConnection'}},
            'errors': None, 'extensions': {}}
        self.assertDictEqual(expected_empty_result, connection_query_result.__dict__)

        # Creating Products for testing not-empty connection
        await create_bulk_of_product(10)
        connection_query_result: ExecutionResult = await self.schema.execute(query_connection)
        connection: dict = connection_query_result.data.get("productConnection")
        connection_nodes = connection.get("edges")

        # Test if product_list len is connection edges len
        database_object_count = await sync_to_async(Product.objects.count)()
        total_count_connection_nodes = connection.get("totalCount")
        self.assertEqual(database_object_count, total_count_connection_nodes)
        # Using the len of the list to make sure ii matches the totalCount
        self.assertEqual(database_object_count, len(connection_nodes))

        # Testing product node query
        first_node = connection_nodes[0].get("node")
        query_product = f"""
        {{
            product(id:"{first_node.get('id')}")
            {{
                {product_node_query_fragment}
            }}
        }}
        """
        product_node_query_result: ExecutionResult = await self.schema.execute(query_product)
        product_node = product_node_query_result.data.get("product")
        # Testing if the object retrieved by the product node is the same of the connection
        self.assertDictEqual(first_node, product_node)
