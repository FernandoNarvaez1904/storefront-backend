from datetime import datetime
from typing import TypedDict

from asgiref.sync import sync_to_async
from django.test import TestCase
from strawberry import ID
from strawberry_django.utils import is_strawberry_type

from storefront_backend.api.relay.node import Node
from users.api.types.user_type import UserType
from users.models import User


class DefaultValuesType(TypedDict):
    id: ID
    username: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool
    is_staff: bool
    last_login: datetime
    date_joined: datetime
    is_active: bool


class TestUserType(TestCase):
    def setUp(self) -> None:
        self.default_values: DefaultValuesType = {
            "id": UserType.encode_id("UserType", "1"),
            "username": "username",
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "email@email.com",
            "is_superuser": False,
            "is_staff": True,
            "last_login": datetime.now(),
            "date_joined": datetime.now(),
            "is_active": True
        }

    async def test_is_gql_type(self) -> None:
        self.assertTrue(is_strawberry_type(UserType))

    async def test_is_node(self) -> None:
        self.assertTrue(issubclass(UserType, Node))

    async def test_username(self) -> None:
        expected: str = self.default_values["username"]
        user_type_username = UserType(**self.default_values).username
        self.assertEqual(user_type_username, expected)

    async def test_first_name(self) -> None:
        expected: str = self.default_values["first_name"]
        user_type_first_name = UserType(**self.default_values).first_name
        self.assertEqual(user_type_first_name, expected)

    async def test_last_name(self) -> None:
        expected: str = self.default_values["last_name"]
        user_type_last_name = UserType(**self.default_values).last_name
        self.assertEqual(user_type_last_name, expected)

    async def test_email(self) -> None:
        expected: str = self.default_values["email"]
        user_type_email = UserType(**self.default_values).email
        self.assertEqual(user_type_email, expected)

    async def test_is_superuser(self) -> None:
        expected: bool = self.default_values["is_superuser"]
        user_type_is_superuser = UserType(**self.default_values).is_superuser
        self.assertEqual(user_type_is_superuser, expected)

    async def test_is_staff(self) -> None:
        expected: bool = self.default_values["is_staff"]
        user_type_is_staff = UserType(**self.default_values).is_staff
        self.assertEqual(user_type_is_staff, expected)

    async def test_last_login(self) -> None:
        expected: datetime = self.default_values["last_login"]
        user_type_last_login = UserType(**self.default_values).last_login
        self.assertEqual(user_type_last_login, expected)

    async def test_date_joined(self) -> None:
        expected: datetime = self.default_values["date_joined"]
        user_type_date_joined = UserType(**self.default_values).date_joined
        self.assertEqual(user_type_date_joined, expected)

    async def test_is_active(self) -> None:
        expected: bool = self.default_values["is_active"]
        user_type_is_active = UserType(**self.default_values).is_active
        self.assertEqual(user_type_is_active, expected)

    async def test_from_model_instance(self) -> None:
        user_input = self.default_values.copy()
        user_input.pop("id")  # type: ignore
        user: User = await sync_to_async(User.objects.create_user)(**user_input, password="hello")
        user_type: UserType = await UserType.from_model_instance(user)

        self.assertEqual(str(user.id), UserType.decode_id(user_type.id)["instance_id"])
        self.assertEqual(user.username, user_type.username)
        self.assertEqual(user.first_name, user_type.first_name)
        self.assertEqual(user.last_name, user_type.last_name)
        self.assertEqual(user.email, user_type.email)
        self.assertEqual(user.is_superuser, user_type.is_superuser)
        self.assertEqual(user.is_staff, user_type.is_staff)
        self.assertEqual(user.is_active, user_type.is_active)
        self.assertEqual(user.date_joined, user_type.date_joined)
