from asgiref.sync import sync_to_async
from django.test import TestCase
from graphql import ExecutionResult
from strawberry import Schema
from strawberry_django_plus.relay import GlobalID

from inventory.api.mutation import Mutation
from inventory.api.query import Query
from inventory.api.types.item import not_in_schema_types
from inventory.models import Item
from inventory.test.api.fragments import item_node_query_fragment
from inventory.test.api.utils import test_mutation, create_bulk_of_item


class InventoryMutationTest(TestCase):
    def setUp(self):
        self.schema = Schema(query=Query, mutation=Mutation, types=not_in_schema_types)

    def test_can_introspect(self):
        self.assertIn("__schema", self.schema.introspect())

    async def test_item_create(self):
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
        user_errors_fragment = """
            field
            message
        """
        mutation_query = f"""
            mutation itemCreate{{
                itemCreate(input:{mutation_input}){{
                    userErrors{{
                        {user_errors_fragment}
                    }}
                    node{{
                        {item_node_query_fragment}
                    }}
                }}
            }}
        """

        item_create_execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        operation_name = "itemCreate"
        await test_mutation(self, item_create_execution_result, operation_name)

        item = item_create_execution_result.data.get(operation_name).get("node")

        # Test if item was actually created
        item_id = item.get("id")
        global_id = GlobalID.from_id(item_id)
        pr_query_set = await sync_to_async(list)(Item.objects.filter(id=global_id.node_id))
        self.assertTrue(pr_query_set)

    async def test_item_deactivate(self):
        item = await create_bulk_of_item(1)
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item[0].id}")
        mutation_query = f"""
            mutation deactivateItem{{
                itemDeactivate(input:{{id:"{item_global_id}"}}){{
                    userErrors{{
                        field
                        message
                    }}
                    node{{
                        {item_node_query_fragment}
                    }}
                }}
            }}
        """

        execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        operation_name = "itemDeactivate"
        await test_mutation(self, execution_result, operation_name)

        # Test if item was changed
        item_changed: Item = await sync_to_async(Item.objects.get)(id=item_global_id.node_id)
        self.assertFalse(item_changed.is_active)

    async def test_item_activate(self):
        item = await create_bulk_of_item(1, active=False)
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item[0].id}")
        mutation_query = f"""
            mutation activateItem{{
                itemActivate(input:{{id:"{item_global_id}"}}){{
                    userErrors{{
                        field
                        message
                    }}
                    node{{
                        {item_node_query_fragment}
                    }}
                }}
            }}
        """

        execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        operation_name = "itemActivate"
        await test_mutation(self, execution_result, operation_name)

        # Test if item was changed
        item_changed: Item = await sync_to_async(Item.objects.get)(id=item_global_id.node_id)
        self.assertTrue(item_changed.is_active)

    async def test_item_update(self):
        item = await sync_to_async(Item.objects.create)(
            name="Product",
            cost=10,
            markup=20,
        )

        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item.id}")

        user_errors_fragment = """
            field
            message
        """
        input_data = '{cost: 43, name: "Updated"}'
        mutation_query = f"""
            mutation updateItem
            {{
                itemUpdate(
                    input: {{ id: "{item_global_id}", data: {input_data} }}
                ) {{
                    __typename
                    userErrors {{
                        {user_errors_fragment}
                    }}
                    node {{
                        {item_node_query_fragment}
                    }}
                }}
            }}
        """

        execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        operation_name = "itemUpdate"
        await test_mutation(self, execution_result, operation_name)

        # Test if item was changed
        item = await sync_to_async(Item.objects.get)(id=item_global_id.node_id)
        self.assertEqual(43, item.cost)
        self.assertEqual("Updated", item.name)

    async def test_item_delete(self):
        item = await create_bulk_of_item(1)
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item[0].id}")

        user_errors_fragment = """
                    field
                    message
                """
        mutation_query = f"""
                    mutation deleteItem
                    {{
                        itemDelete(
                            input: {{ id: "{item_global_id}" }}
                        ) {{
                            __typename
                            userErrors {{
                                {user_errors_fragment}
                            }}
                            node {{
                                id
                            }}
                        }}
                    }}
                """
        execution_result: ExecutionResult = await self.schema.execute(mutation_query)

        operation_name = "itemDelete"
        await test_mutation(self, execution_result, operation_name)

        # Test if item was deleted
        item = await sync_to_async(Item.objects.filter)(id=item_global_id.node_id)
        item_count = await sync_to_async(item.count)()
        self.assertEqual(0, item_count)
