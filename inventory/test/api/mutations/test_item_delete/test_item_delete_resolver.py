from typing import List

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from inventory.api.mutations.item_delete.item_delete_input import ItemDeleteInput
from inventory.api.mutations.item_delete.item_delete_payload import ItemDeletePayload
from inventory.api.mutations.item_delete.item_delete_resolver import item_delete_resolver
from inventory.api.types.item import ItemType
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.schema import schema
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list
from storefront_backend.tests.utils import get_async_request_with_user_and_session, create_user_with_permission
from users.models import User


class ItemDeleteResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1)
        self.item = temp[0]

        self.mutation_query = """
            mutation ItemDelete($input: ItemDeleteInput!) {
              itemDelete(input: $input) {
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
            "id": async_to_sync(ItemType.get_id_from_model_instance)(self.item)
        }}

    async def test_item_delete_resolver_response(self) -> None:
        id_node = ItemType.encode_id(f"{self.item.id}")
        item_input = ItemDeleteInput(id=id_node)
        result: ItemDeletePayload = await item_delete_resolver(item_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemDeletePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        self.assertIsNotNone(result.node)
        if result.node:
            # Test if id is not null
            self.assertIsNotNone(result.node.id)

            # Test if item is the same that input
            self.assertEqual(result.node.id, id_node)

    async def test_item_delete_resolver_side_effect(self) -> None:
        # Building input
        id_node = ItemType.encode_id(f"{self.item.id}")
        item_input = ItemDeleteInput(id=id_node)

        # Updating is_active
        await item_delete_resolver(item_input)

        # Checking if item was deleted
        item = await get_lazy_query_set_as_list(Item.objects.filter(pk=self.item.id))
        self.assertFalse(item)

    async def test_item_delete_resolver_permission_denied(self) -> None:
        user = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["itemDelete"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_item_delete_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "delete_item")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["itemDelete"]["userErrors"]
            self.assertFalse(user_errors)
