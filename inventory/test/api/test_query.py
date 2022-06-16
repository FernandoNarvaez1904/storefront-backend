from asgiref.sync import sync_to_async
from django.test import TestCase
from strawberry import Schema
from strawberry.types import ExecutionResult
from strawberry_django_plus.relay import GlobalID

from inventory.api.query import Query
from inventory.api.types.item import ItemType
from inventory.models import Item
from inventory.test.api.fragments import item_node_query_fragment
from inventory.test.api.utils import test_relay_connection, get_connection_query, create_bulk_of_item


class InventoryQueryTest(TestCase):
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
        total_count = connection.get("totalCount")
        database_object_count = await sync_to_async(Item.objects.count)()
        self.assertEqual(database_object_count, total_count)

        # Using the len of the list to make sure ii matches the totalCount
        self.assertEqual(database_object_count, len(connection.get("edges")))

    async def test_item_node(self):
        item = await create_bulk_of_item(1)
        item_global_id = GlobalID(node_id=f"{item[0].id}", type_name=ItemType.__name__)
        # Testing item node query
        query_item = f"""
        {{
            item(id:"{item_global_id}")
            {{
                {item_node_query_fragment}
            }}
        }}
        """
        item_node_query_result: ExecutionResult = await self.schema.execute(query_item)
        item_node = item_node_query_result.data.get("item")

        self.assertIsNotNone(item_node)
        # Testing if the object retrieved by the item node is the same
        self.assertEqual(str(item_global_id), item_node.get("id"))

        # Testing a connection inside the query
        await test_relay_connection(test_case=self, exec_result_data=item_node.get("itemVersions"))
