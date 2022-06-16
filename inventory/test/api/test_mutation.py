from asgiref.sync import sync_to_async
from django.test import TestCase
from graphql import ExecutionResult
from strawberry import Schema
from strawberry_django_plus.relay import GlobalID

from inventory.api.mutation import Mutation
from inventory.api.query import Query
from inventory.api.types.item import not_in_schema_types
from inventory.models import Item, ItemDetail
from inventory.test.api.fragments import item_node_query_fragment


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
        item_fragment = """
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

        # Test has no execution errors
        self.assertIsNone(item_create_execution_result.errors)

        # Test data is not null
        exec_result_data: dict = item_create_execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        item_create_mutation_result: dict = exec_result_data.get("itemCreate")
        self.assertIsNotNone(item_create_mutation_result)

        # Test if UserError is returned
        user_errors: List = item_create_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if item is returned
        item: dict = item_create_mutation_result.get("node")
        self.assertIsNotNone(item)

        # Test if all fields return
        self.assertNotIn(None, item.values())

        # Test if item was actually created
        item_id = item.get("id")
        global_id = GlobalID.from_id(item_id)
        pr_query_set = await sync_to_async(list)(Item.objects.filter(id=global_id.node_id))
        self.assertTrue(pr_query_set)

    async def test_item_deactivate(self):
        item = await sync_to_async(Item.objects.create)()
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item.id}")
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

        # Test has no execution error
        self.assertIsNone(execution_result.errors)

        # Test data is not null
        exec_result_data: dict = execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        item_deactivate_mutation_result: dict = exec_result_data.get("itemDeactivate")
        self.assertIsNotNone(item_deactivate_mutation_result)

        # Test if UserError is returned
        user_errors: List = item_deactivate_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if item is returned
        item_type_result: dict = item_deactivate_mutation_result.get("node")
        self.assertIsNotNone(item_type_result)

        # Test if all fields return
        self.assertNotIn(None, item_type_result.values())

        # Test if item was changed
        item_changed: Item = await sync_to_async(Item.objects.get)(id=item_global_id.node_id)
        self.assertFalse(item_changed.is_active)

    async def test_item_activate(self):
        item = await sync_to_async(Item.objects.create)(
            is_active=False
        )
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item.id}")
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

        # Test has no execution error
        self.assertIsNone(execution_result.errors)

        # Test data is not null
        exec_result_data: dict = execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        item_item_mutation_result: dict = exec_result_data.get("itemActivate")
        self.assertIsNotNone(item_item_mutation_result)

        # Test if UserError is returned
        user_errors: List = item_item_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if item is returned
        item_type_result: dict = item_item_mutation_result.get("node")
        self.assertIsNotNone(item_type_result)

        # Test if all fields return
        self.assertNotIn(None, item_type_result.values())

        # Test if item was changed
        item_changed: Item = await sync_to_async(Item.objects.get)(id=item_global_id.node_id)
        self.assertTrue(item_changed.is_active)

    async def test_item_update(self):
        item = await sync_to_async(Item.objects.create)()
        await sync_to_async(ItemDetail.objects.create)(
            name="Product",
            cost=10,
            markup=20,
            root_item=item
        )
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item.id}")

        item_fragment = """
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

        # Test has no execution error
        self.assertIsNone(execution_result.errors)

        # Test data is not null
        exec_result_data: dict = execution_result.data
        self.assertIsNotNone(exec_result_data)

        # Test Mutation Result Exist
        item_item_mutation_result: dict = exec_result_data.get("itemUpdate")
        self.assertIsNotNone(item_item_mutation_result)

        # Test if UserError is returned
        user_errors: List = item_item_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if item is returned
        item_type_result: dict = item_item_mutation_result.get("node")
        self.assertIsNotNone(item_type_result)

        # Test if all fields return
        self.assertNotIn(None, item_type_result.values())

        # Test if item was changed
        item = await sync_to_async(Item.objects.get)(id=item_global_id.node_id)
        item_detail_changed: ItemDetail = await sync_to_async(ItemDetail.objects.get)(id=item.current_detail_id)
        self.assertEqual(43, item_detail_changed.cost)
        self.assertEqual("Updated", item_detail_changed.name)

    async def test_item_delete(self):
        item = await sync_to_async(Item.objects.create)()
        await sync_to_async(ItemDetail.objects.create)(
            name="Product",
            cost=10,
            markup=20,
            root_item=item
        )
        item_global_id = GlobalID(type_name='ItemType', node_id=f"{item.id}")

        item_fragment = """
                    id
                    __typename
                """
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
                                {item_fragment}
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
        item_item_mutation_result: dict = exec_result_data.get("itemDelete")
        self.assertIsNotNone(item_item_mutation_result)

        # Test if UserError is returned
        user_errors: List = item_item_mutation_result.get("userErrors")
        self.assertIsNotNone(user_errors)

        # Test Mutation Result UserError is empty
        self.assertFalse(len(user_errors))

        # Test if item is returned
        item_type_result: dict = item_item_mutation_result.get("node")
        self.assertIsNotNone(item_type_result)

        # Test if all fields return
        self.assertNotIn(None, item_type_result.values())

        # Test if item was deleted
        item = await sync_to_async(Item.objects.filter)(id=item_global_id.node_id)
        item_count = await sync_to_async(item.count)()
        self.assertEqual(0, item_count)
