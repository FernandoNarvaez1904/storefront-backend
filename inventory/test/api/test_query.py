from typing import List

from asgiref.sync import sync_to_async
from django.test import TestCase
from strawberry import Schema
from strawberry.types import ExecutionResult

from inventory.api.query import Query
from inventory.models import Item, ItemDetail


async def create_bulk_of_item(num: int) -> List[Item]:
    item_list = []
    for i in range(num):
        item = await sync_to_async(Item.objects.create)(sku=i)

        await sync_to_async(ItemDetail.objects.create)(
            name=f"itemDetail{i}",
            barcode="890432",
            cost=10,
            markup=50,
            root_item=item,
        )
        item_list.append(item)
    return item_list


class InventoryQueryTest(TestCase):
    def setUp(self):
        self.schema = Schema(query=Query)

    def test_can_introspect(self):
        self.assertIn("__schema", self.schema.introspect())

    # I tested the item_connection and item in the same test, because
    # I needed the same database objects for the global id.
    async def test_item_queries(self):
        item_node_query_fragment = """
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
          itemConnection(
            # Args were included to test if they exist
            before: null
            after: null
            first: null
            last: null
          ){{
            edges{{
              cursor
              node{{
                {item_node_query_fragment}
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
            'data': {'itemConnection': {'edges': [], 'totalCount': 0, '__typename': 'ItemTypeConnection'}},
            'errors': None, 'extensions': {}}
        self.assertDictEqual(expected_empty_result, connection_query_result.__dict__)

        # Creating Items for testing not-empty connection
        await create_bulk_of_item(10)
        connection_query_result: ExecutionResult = await self.schema.execute(query_connection)
        connection: dict = connection_query_result.data.get("itemConnection")
        connection_nodes = connection.get("edges")

        # Test if item_list len is connection edges len
        database_object_count = await sync_to_async(Item.objects.count)()
        total_count_connection_nodes = connection.get("totalCount")
        self.assertEqual(database_object_count, total_count_connection_nodes)
        # Using the len of the list to make sure ii matches the totalCount
        self.assertEqual(database_object_count, len(connection_nodes))

        # Testing item node query
        first_node = connection_nodes[0].get("node")
        query_item = f"""
        {{
            item(id:"{first_node.get('id')}")
            {{
                {item_node_query_fragment}
            }}
        }}
        """
        item_node_query_result: ExecutionResult = await self.schema.execute(query_item)
        item_node = item_node_query_result.data.get("item")
        # Testing if the object retrieved by the item node is the same of the connection
        self.assertDictEqual(first_node, item_node)
