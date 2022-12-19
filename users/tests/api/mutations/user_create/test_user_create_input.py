from typing import List

from django.test import TransactionTestCase

from storefront_backend.api.types import UserError
from users.api.mutations.user_create.user_create_errors import CannotCreateUserUsernameIsNotUnique, \
    CannotCreateUserEmailIsNotUnique
from users.api.mutations.user_create.user_create_input import UserCreateInput
from users.models import User


class TestUserCreateInput(TransactionTestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user("username", "email@email.com", password="pswd")
        self.default_values = {
            "password": "pws",
            "first_name": "First",
            "last_name": "Last",
            "email": "unleash@gmail.com",
            "username": "unleash"
        }

    async def test_validate_and_get_errors_username(self) -> None:
        input_repeated_username = UserCreateInput(**{**self.default_values, "username": self.user.username})
        username_error_payload: List[UserError] = await input_repeated_username.validate_and_get_errors()
        self.assertIsInstance(username_error_payload[0], CannotCreateUserUsernameIsNotUnique)

    async def test_validate_and_get_errors_email(self) -> None:
        input_repeated_email = UserCreateInput(**{**self.default_values, "email": self.user.email})
        email_error_payload: List[UserError] = await input_repeated_email.validate_and_get_errors()
        self.assertIsInstance(email_error_payload[0], CannotCreateUserEmailIsNotUnique)

    async def test_validate_and_get_errors_all(self) -> None:
        input_all_errors = UserCreateInput(
            **{**self.default_values, "email": self.user.email, "username": self.user.username})
        all_error_payload: List[UserError] = await input_all_errors.validate_and_get_errors()
        self.assertIsInstance(all_error_payload[0], CannotCreateUserUsernameIsNotUnique)
        self.assertIsInstance(all_error_payload[1], CannotCreateUserEmailIsNotUnique)

    async def test_validate_and_get_errors_no_errors(self) -> None:
        input_no_errors = UserCreateInput(**self.default_values)
        all_error_payload: List[UserError] = await input_no_errors.validate_and_get_errors()
        self.assertFalse(all_error_payload)
