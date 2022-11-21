from typing import List

from django.test import TransactionTestCase

from storefront_backend.api.types import UserError
from users.api.mutations.user_login.user_login_errors import CannotLoginUsernameDoesNotExist, \
    CannotLoginPasswordIsNotCorrect
from users.api.mutations.user_login.user_login_input import UserLoginInput
from users.models import User


class TestUserLoginsInput(TransactionTestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user("username", "email@email.com", password="pswd")
        self.default_values = {
            "password": "pswd",
            "username": "username"
        }

    async def test_validate_and_get_errors_not_valid_username(self) -> None:
        not_valid_username_input = UserLoginInput(**{**self.default_values, "username": "something"})
        username_error_payload: List[UserError] = await not_valid_username_input.validate_and_get_errors()
        self.assertIsInstance(username_error_payload[0], CannotLoginUsernameDoesNotExist)

    async def test_validate_and_get_errors_not_valid_password(self) -> None:
        not_valid_password_input = UserLoginInput(**{**self.default_values, "password": "123456"})
        password_error_payload: List[UserError] = await not_valid_password_input.validate_and_get_errors()
        self.assertIsInstance(password_error_payload[0], CannotLoginPasswordIsNotCorrect)
