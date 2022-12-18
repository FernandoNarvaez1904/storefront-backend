from typing import List, TypedDict, cast

from django.contrib.auth.models import Permission
from django.test import TestCase
from strawberry import ID
from strawberry_django.utils import is_strawberry_type

from storefront_backend.api.relay.node import Node
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list
from users.api.types.permission_type import PermissionType


class PermissionTypeDefaultValues(TypedDict):
    id: ID
    name: str
    codename: str


class TestPermissionType(TestCase):
    def setUp(self) -> None:
        self.default_values: PermissionTypeDefaultValues = {
            "id": cast(ID, "1"),
            "name": "permission",
            "codename": "perm"
        }

    async def test_is_gql_type(self) -> None:
        self.assertTrue(is_strawberry_type(PermissionType))

    async def test_is_node(self) -> None:
        self.assertTrue(issubclass(PermissionType, Node))

    async def test_name(self) -> None:
        permission_type_name = PermissionType(**self.default_values).name
        expected: str = self.default_values["name"]
        self.assertEqual(permission_type_name, expected)

    async def test_codename(self) -> None:
        permission_type_codename = PermissionType(**self.default_values).codename
        expected: str = self.default_values["codename"]
        self.assertEqual(permission_type_codename, expected)

    async def test_from_model_instance(self) -> None:
        permissions_filtered: List[Permission] = await get_lazy_query_set_as_list(
            Permission.objects.filter(codename="add_permission"))
        permission: Permission = permissions_filtered[0]
        permission_type = await PermissionType.from_model_instance(permission)

        self.assertIsNotNone(permission_type.id)
        self.assertEqual(permission_type.codename, "add_permission")
        self.assertEqual(permission_type.name, "Can add permission")
