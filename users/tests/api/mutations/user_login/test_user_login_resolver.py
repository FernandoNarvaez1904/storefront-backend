import datetime
from pathlib import Path
from typing import cast

from django.contrib.sessions.middleware import SessionMiddleware
from django.core.handlers.asgi import ASGIRequest
from django.test import TransactionTestCase, AsyncRequestFactory  # type: ignore
from django.utils import timezone
from graphql import GraphQLResolveInfo, OperationDefinitionNode
from strawberry.types import Info

from users.api.mutations.user_login.user_login_input import UserLoginInput
from users.api.mutations.user_login.user_login_payload import UserLoginPayload
from users.api.mutations.user_login.user_login_resolver import user_login_resolver
from users.models import User


class UserLoginResolverTest(TransactionTestCase):

    # Do not type. MYPY will scream at you
    def setUp(self):
        self.input = {
            "password": "pws",
            "username": "unleash"
        }
        self.user = User.objects.create_user(**self.input)

        # Faking Request
        async_request = AsyncRequestFactory().post("/graphql")
        middleware = SessionMiddleware(lambda x: x)
        middleware.process_request(async_request)

        def f() -> bool:
            return False

        # Faking Info for resolver
        resolver_info = GraphQLResolveInfo(
            context={},
            root_value=None,
            variable_values={},
            fragments={},
            field_name="",
            operation=OperationDefinitionNode(),
            field_nodes=[],
            is_awaitable=f,
            return_type=None,
            parent_type=None,
            schema=None,
            path=Path()
        )
        resolver_info.context["request"] = async_request
        self.info: Info = Info(_raw_info=resolver_info, _field=None)

    async def test_user_login_resolver_response(self):
        user_login_input = UserLoginInput(**self.input)
        result: UserLoginPayload = cast(UserLoginPayload,
                                        await user_login_resolver(input=user_login_input, info=self.info))

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, UserLoginPayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        self.assertIsNotNone(result.node.id)

        # Test if user is is_active
        self.assertTrue(result.node.is_active)

        # Test if last_login registered
        self.assertAlmostEqual(result.node.last_login, timezone.now(),
                               delta=datetime.timedelta(seconds=0.5))

        # Test id the right user was logged in
        self.assertEqual(self.input.get("username"), result.node.username)

    async def test_item_login_resolver_side_effect(self):
        user_login_input = UserLoginInput(**self.input)
        request: ASGIRequest = self.info.context.get("request")

        await user_login_resolver(input=user_login_input, info=self.info)

        # Check of user is logged in
        self.assertTrue(request.session.session_key)
