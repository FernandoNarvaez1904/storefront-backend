import datetime

from django.test import TestCase
from strawberry_django.utils import is_strawberry_type, is_django_type
from strawberry_django_plus import gql

from users.api.types.user_type import UserType


class UserTypeTest(TestCase):
    def setUp(self):
        self.default_values = {
            "username": "username",
            "first_name": "FirstName",
            "last_name": "LastName",
            "email": "email@email.com",
            "is_superuser": False,
            "is_staff": True,
            "last_login": datetime.datetime.now(),
            "date_joined": datetime.datetime.now()
        }

    def test_is_gql_type(self):
        self.assertTrue(is_strawberry_type(UserType))

    def test_is_node(self):
        self.assertTrue(issubclass(UserType, gql.Node))

    def test_is_django_strawberry_type(self):
        self.assertTrue(is_django_type(UserType))

    def test_username(self):
        expected: str = self.default_values.get("username")
        user_type_username = UserType(**self.default_values).username
        self.assertEqual(user_type_username, expected)

    def test_first_name(self):
        expected: str = self.default_values.get("first_name")
        user_type_first_name = UserType(**self.default_values).first_name
        self.assertEqual(user_type_first_name, expected)

    def test_last_name(self):
        expected: str = self.default_values.get("last_name")
        user_type_last_name = UserType(**self.default_values).last_name
        self.assertEqual(user_type_last_name, expected)

    def test_email(self):
        expected: str = self.default_values.get("email")
        user_type_email = UserType(**self.default_values).email
        self.assertEqual(user_type_email, expected)

    def test_is_superuser(self):
        expected: str = self.default_values.get("is_superuser")
        user_type_is_superuser = UserType(**self.default_values).is_superuser
        self.assertEqual(user_type_is_superuser, expected)

    def test_is_staff(self):
        expected: str = self.default_values.get("is_staff")
        user_type_is_staff = UserType(**self.default_values).is_staff
        self.assertEqual(user_type_is_staff, expected)

    def test_last_login(self):
        expected: str = self.default_values.get("last_login")
        user_type_last_login = UserType(**self.default_values).last_login
        self.assertEqual(user_type_last_login, expected)

    def test_date_joined(self):
        expected: str = self.default_values.get("date_joined")
        user_type_date_joined = UserType(**self.default_values).date_joined
        self.assertEqual(user_type_date_joined, expected)
