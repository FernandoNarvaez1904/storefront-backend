import datetime

from asgiref.sync import sync_to_async
from django.test import TestCase
from strawberry_django.utils import is_strawberry_type

from storefront_backend.api.relay.node import Node
from users.api.types.user_type import UserType
from users.models import User


class TestUserType(TestCase):
    def setUp(self):
        self.default_values = {
            "id": "1",
            "username": "username",
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "email@email.com",
            "is_superuser": False,
            "is_staff": True,
            "last_login": datetime.datetime.now(),
            "date_joined": datetime.datetime.now(),
            "is_active": True
        }

    async def test_is_gql_type(self):
        self.assertTrue(is_strawberry_type(UserType))

    async def test_is_node(self):
        self.assertTrue(issubclass(UserType, Node))

    async def test_username(self):
        expected: str = self.default_values.get("username")
        user_type_username = UserType(**self.default_values).username
        self.assertEqual(user_type_username, expected)

    async def test_first_name(self):
        expected: str = self.default_values.get("first_name")
        user_type_first_name = UserType(**self.default_values).first_name
        self.assertEqual(user_type_first_name, expected)

    async def test_last_name(self):
        expected: str = self.default_values.get("last_name")
        user_type_last_name = UserType(**self.default_values).last_name
        self.assertEqual(user_type_last_name, expected)

    async def test_email(self):
        expected: str = self.default_values.get("email")
        user_type_email = UserType(**self.default_values).email
        self.assertEqual(user_type_email, expected)

    async def test_is_superuser(self):
        expected: str = self.default_values.get("is_superuser")
        user_type_is_superuser = UserType(**self.default_values).is_superuser
        self.assertEqual(user_type_is_superuser, expected)

    async def test_is_staff(self):
        expected: str = self.default_values.get("is_staff")
        user_type_is_staff = UserType(**self.default_values).is_staff
        self.assertEqual(user_type_is_staff, expected)

    async def test_last_login(self):
        expected: str = self.default_values.get("last_login")
        user_type_last_login = UserType(**self.default_values).last_login
        self.assertEqual(user_type_last_login, expected)

    async def test_date_joined(self):
        expected: str = self.default_values.get("date_joined")
        user_type_date_joined = UserType(**self.default_values).date_joined
        self.assertEqual(user_type_date_joined, expected)

    async def test_is_active(self):
        expected: str = self.default_values.get("is_active")
        user_type_is_active = UserType(**self.default_values).is_active
        self.assertEqual(user_type_is_active, expected)

    async def test_from_model_instance(self) -> None:
        user: User = await sync_to_async(User.objects.create_user)(**self.default_values, password="hello")
        user_type: UserType = UserType.from_model_instance(user)

        self.assertEqual(str(user.id), UserType.decode_id(user_type.id)["instance_id"])
        self.assertEqual(user.username, user_type.username)
        self.assertEqual(user.first_name, user_type.first_name)
        self.assertEqual(user.last_name, user_type.last_name)
        self.assertEqual(user.email, user_type.email)
        self.assertEqual(user.is_superuser, user_type.is_superuser)
        self.assertEqual(user.is_staff, user_type.is_staff)
        self.assertEqual(user.is_active, user_type.is_active)
        self.assertEqual(user.date_joined, user_type.date_joined)
