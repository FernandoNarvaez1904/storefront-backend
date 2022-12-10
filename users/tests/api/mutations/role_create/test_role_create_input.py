from typing import List, TypedDict

from django.contrib.auth.models import Group, Permission
from django.test import TransactionTestCase
from strawberry import ID

from storefront_backend.api.types import UserError
from users.api.mutations.role_create.role_create_errors import CannotCreateRoleNameIsNotUnique, \
    CannotCreateRolePermissionDoesNotExist
from users.api.mutations.role_create.role_create_input import RoleCreateInput
from users.api.types.permission_type import PermissionType


class DefaultValuesType(TypedDict):
    name: str
    permissions_ids: List[ID]


class TestRoleCreateInput(TransactionTestCase):

    def setUp(self) -> None:
        self.role: Group = Group.objects.create(name="Role1")

        if not self.role.permissions.count():
            perm = Permission.objects.all()
            self.role.permissions.add(perm[0], perm[1])

        self.default_values: DefaultValuesType = {
            "name": "Role2",
            "permissions_ids": [PermissionType.encode_id("PermissionType", "1"),
                                PermissionType.encode_id("PermissionType", "2")]
        }

    async def test_validate_and_get_errors_name(self) -> None:
        input_repeated_name = RoleCreateInput(name=self.role.name,
                                              permissions_ids=self.default_values["permissions_ids"])
        name_error_payload: List[UserError] = await input_repeated_name.validate_and_get_errors()
        self.assertIsInstance(name_error_payload[0], CannotCreateRoleNameIsNotUnique)

    async def test_validate_and_get_errors_perm(self) -> None:
        input_non_existent_perm = RoleCreateInput(name=self.default_values["name"],
                                                  permissions_ids=[PermissionType.encode_id("PermissionType", "1000")])
        perm_error_payload: List[UserError] = await input_non_existent_perm.validate_and_get_errors()
        self.assertIsInstance(perm_error_payload[0], CannotCreateRolePermissionDoesNotExist)

    async def test_validate_and_get_errors_all(self) -> None:
        all_error_input = RoleCreateInput(name=self.role.name,
                                          permissions_ids=[PermissionType.encode_id("PermissionType", "1000")])
        all_error_payload: List[UserError] = await all_error_input.validate_and_get_errors()
        self.assertIsInstance(all_error_payload[0], CannotCreateRoleNameIsNotUnique)
        self.assertIsInstance(all_error_payload[1], CannotCreateRolePermissionDoesNotExist)
