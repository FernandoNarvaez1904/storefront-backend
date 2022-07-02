from django.test import TestCase
from strawberry_django.utils import is_strawberry_type, is_django_type
from strawberry_django_plus import gql

from users.api.types.user_type import UserType
from users.models import User


class UserTypeTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="username",
            is_superuser=False,
            first_name="FirstName",
            last_name="LastName",
            email="email@email.com",
            is_staff=False,
            password="password"
        )
        self.user = user

    def test_is_gql_type(self):
        self.assertTrue(is_strawberry_type(UserType))

    def test_is_node(self):
        self.assertTrue(issubclass(UserType, gql.Node))

    def test_is_django_strawberry_type(self):
        self.assertTrue(is_django_type(UserType))

    def test_username(self):
        expected: str = "username"
        user_type_username = UserType(username=expected).username
        self.assertEqual(user_type_username, expected)
