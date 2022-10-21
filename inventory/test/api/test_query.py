from asgiref.sync import sync_to_async
from django.test import TransactionTestCase
from strawberry import Schema
from strawberry.types import ExecutionResult

from inventory.api.query import Query
from inventory.models import Item
from inventory.test.api.fragments import item_node_query_fragment
from inventory.test.api.utils import test_relay_connection, get_connection_query, create_bulk_of_item


class InventoryQueryTest(TransactionTestCase):
    def setUp(self):
        self.schema = Schema(query=Query)

    def test_can_introspect(self):
        self.assertIn("__schema", self.schema.introspect())

    async def test_item_queries(self):
        operation_name = "itemConnection"
        query_connection = f"{{ {await sync_to_async(get_connection_query)(item_node_query_fragment, operation_name)} }}"

        # Creating Items for testing not-empty connection
        await create_bulk_of_item(10)
        execution_result: ExecutionResult = await self.schema.execute(query_connection)
        execution_result = await test_relay_connection(self, execution_result=execution_result,
                                                       operation_name=operation_name)
        connection = execution_result.data.get(operation_name)

        # Test if item_list len is connection edges len
        total_count = connection.get("pageInfo").get("totalCount")
        database_object_count = await sync_to_async(Item.objects.count)()
        self.assertEqual(database_object_count, total_count)

        # Using the len of the list to make sure ii matches the totalCount
        self.assertEqual(database_object_count, len(connection.get("edges")))

    async def test_item_filter_query(self):
        seed = "seed"
        operation_name = "itemConnection"

        l = await create_bulk_of_item(10)
        l2 = await create_bulk_of_item(5, seed=seed)

        filter_query = f"""
            filter: {{
                sku:{{
                    contains: "{seed}"
                }}
                 name : {{
                        contains: "{seed}"
                    }}
            }}
        """
        query_connection = f"{{ {await sync_to_async(get_connection_query)(item_node_query_fragment, operation_name, filter_query)} }}"
        execution_result: ExecutionResult = await self.schema.execute(query_connection)
        execution_result = await test_relay_connection(self, execution_result=execution_result,
                                                       operation_name=operation_name)

        connection = execution_result.data.get(operation_name)

        # Test if item_list len is connection edges len
        total_count = connection.get("pageInfo").get("edgesCount")
        filtered_database_qs = await sync_to_async(list)(Item.objects.filter(sku__contains=seed))
        self.assertEqual(len(filtered_database_qs), total_count)
