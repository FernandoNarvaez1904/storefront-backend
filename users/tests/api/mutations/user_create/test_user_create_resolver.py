import datetime
from typing import List

from django.test import TransactionTestCase
from django.utils import timezone
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from storefront_backend.api.schema import schema
from storefront_backend.tests.utils import create_user_with_permission, get_async_request_with_user_and_session
from users.api.mutations.user_create.user_create_input import UserCreateInput
from users.api.mutations.user_create.user_create_payload import UserCreatePayload
from users.api.mutations.user_create.user_create_resolver import user_create_resolver
from users.models import User


class UserCreateResolverTest(TransactionTestCase):

    def setUp(self) -> None:
        self.input = {
            "password": "pws",
            "first_name": "First",
            "last_name": "Last",
            "email": "unleash@gmail.com",
            "username": "unleash"
        }
        self.mutation_query = """
            mutation UserCreate($input: UserCreateInput!) {
              userCreate(input: $input) {
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
            "password": "pws",
            "firstName": "First",
            "lastName": "Last",
            "email": "unleash@gmail.com",
            "username": "unleash"
        }}

    async def test_user_create_resolver_response(self):
        user_create_input = UserCreateInput(**self.input)
        result: UserCreatePayload = await user_create_resolver(input=user_create_input)

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, UserCreatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if user is is_active
        self.assertTrue(result.node.is_active)

        # Test if no special permission were granted
        self.assertFalse(result.node.is_superuser)
        self.assertFalse(result.node.is_staff)

        # Test if date_joined is correct
        self.assertAlmostEqual(result.node.date_joined, timezone.now(),
                               delta=datetime.timedelta(seconds=0.5))

        # Test that no login happened
        self.assertIsNone(result.node.last_login)

        self.input.pop("password")
        # Test if response has all input data
        for key, value in self.input.items():
            self.assertEqual(value, result.node.__getattribute__(key))

    async def test_user_create_resolver_side_effect(self):
        # Building input
        user_create_input = UserCreateInput(**self.input)

        # Creating user
        await user_create_resolver(input=user_create_input)

        # Checking if field was updated in database
        self.input.pop("password")
        does_user_exist = await User.objects.filter(**self.input).aexists()
        self.assertTrue(does_user_exist)

    async def test_user_create_resolver_permission_denied(self) -> None:
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["userCreate"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_user_create_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "add_user")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["userCreate"]["userErrors"]
            self.assertFalse(user_errors)
