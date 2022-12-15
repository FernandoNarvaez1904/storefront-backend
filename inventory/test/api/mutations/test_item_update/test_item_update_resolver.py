from typing import List, TypedDict

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from inventory.api.mutations.item_update.Item_update_resolver import item_update_resolver
from inventory.api.mutations.item_update.item_update_input import ItemUpdateInput, ItemUpdateDataInput
from inventory.api.mutations.item_update.item_update_payload import ItemUpdatePayload
from inventory.api.types.item import ItemType
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.schema import schema
from storefront_backend.tests.utils import get_async_request_with_user_and_session, create_user_with_permission
from users.models import User


class DefaultValuesType(TypedDict):
    name: str
    cost: float


class ItemUpdateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1)
        self.item = temp[0]
        self.new_data: DefaultValuesType = {
            "name": "new_name",
            "cost": 10.50
        }

        self.mutation_query = """
            mutation ItemUpdate($input: ItemUpdateInput!) {
              itemUpdate(input: $input) {
                node {
                  id
                }
                userErrors {
                  field
                  message
                }
              }
            }
        """
        self.mutation_variables = {"input": {
            "id": async_to_sync(ItemType.get_id_from_model_instance)(self.item),
            "data": {
                "name": "second_name"
            }
        }}

    async def test_item_update_resolver_response(self) -> None:
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        update_data = ItemUpdateDataInput(**self.new_data)
        item_update_input = ItemUpdateInput(id=id_node, data=update_data)

        result: ItemUpdatePayload = await item_update_resolver(item_update_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemUpdatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        self.assertIsNotNone(result.node)
        if result.node:
            # Test if id is not null
            self.assertIsNotNone(result.node.id)

            # Test if item is the same that input
            self.assertEqual(result.node.id, id_node)

            # test if data was updated according to update_data
            for key, value in self.new_data.items():
                self.assertEqual(value, result.node.__getattribute__(key))

    async def test_item_update_resolver_side_effect(self) -> None:
        # Building input
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        update_data = ItemUpdateDataInput(**self.new_data)
        item_update_input = ItemUpdateInput(id=id_node, data=update_data)

        # Updating is_active
        await item_update_resolver(item_update_input)

        # test if data was updated according to update_data
        item = await Item.objects.aget(pk=self.item.id)
        for key, value in self.new_data.items():
            self.assertEqual(value, item.__getattribute__(key))

    async def test_item_update_resolver_permission_denied(self) -> None:
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["itemUpdate"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_item_update_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "change_item")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["itemUpdate"]["userErrors"]
            self.assertFalse(user_errors)
