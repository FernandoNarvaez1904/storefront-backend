from typing import List

from asgiref.sync import async_to_sync
from django.test import TransactionTestCase
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from inventory.api.mutations.item_deactivate.item_deactivate_input import ItemDeactivateInput
from inventory.api.mutations.item_deactivate.item_deactivate_payload import ItemDeactivatePayload
from inventory.api.mutations.item_deactivate.item_deactivate_resolver import item_deactivate_resolver
from inventory.api.types.item import ItemType
from inventory.models import Item
from inventory.test.api.utils import create_bulk_of_item
from storefront_backend.api.relay.node import Node
from storefront_backend.api.schema import schema
from storefront_backend.tests.utils import create_user_with_permission, get_async_request_with_user_and_session
from users.models import User


class ItemDeactivateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        temp: List[Item] = async_to_sync(create_bulk_of_item)(1)
        self.item = temp[0]

        self.mutation_query = """
            mutation ItemDeactivate($input: ItemDeactivateInput!) {
              itemDeactivate(input: $input) {
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
        }}

    async def test_item_deactivate_resolver_response(self):
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemDeactivateInput(id=id_node)
        result: ItemDeactivatePayload = await item_deactivate_resolver(item_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, ItemDeactivatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if item is the same that input
        self.assertEqual(result.node.id, id_node)

        # Test if item is not is_active
        self.assertFalse(result.node.is_active)

    async def test_item_deactivate_resolver_side_effect(self):
        # Building input
        id_node = Node.encode_id("ItemType", f"{self.item.id}")
        item_input = ItemDeactivateInput(id=id_node)

        # Updating is_active
        await item_deactivate_resolver(item_input)

        # Checking if field was updated in database
        item = await Item.objects.aget(pk=self.item.id)
        self.assertFalse(item.is_active)

    async def test_item_deactivate_resolver_permission_denied(self) -> None:
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["itemDeactivate"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_item_deactivate_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "activate_item")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["itemDeactivate"]["userErrors"]
            self.assertFalse(user_errors)
