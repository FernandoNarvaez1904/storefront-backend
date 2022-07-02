from django.test import TestCase
from strawberry_django.utils import is_strawberry_type, is_django_type
from strawberry_django_plus import gql

from users.api.types.user_type import UserType


class UserTypeTest(TestCase):
    def setUp(self):
        self.default_values = {
            "username": "username",
            "first_name": "FirstName",
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
