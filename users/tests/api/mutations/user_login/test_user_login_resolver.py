import datetime
from typing import cast

import strawberry
from django.core.handlers.asgi import ASGIRequest
from django.test import TransactionTestCase, AsyncRequestFactory  # type: ignore
from django.utils import timezone
from strawberry.types import Info

from storefront_backend.api.mutation import Mutation
from storefront_backend.tests.utils import get_info
from users.api.mutations.user_login.user_login_input import UserLoginInput
from users.api.mutations.user_login.user_login_payload import UserLoginPayload
from users.api.mutations.user_login.user_login_resolver import user_login_resolver
from users.models import User


class UserLoginResolverTest(TransactionTestCase):

    # Do not type. MYPY will scream at you
    def setUp(self) -> None:
        self.input = {
            "password": "pws",
            "username": "unleash"
        }
        self.user = User.objects.create_user(**self.input)
        self.info: Info = get_info(strawberry.field(resolver=user_login_resolver), "user_login_resolver",
                                   UserLoginPayload, Mutation)

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
