from typing import List, TypedDict

from django.contrib.auth.models import Group, Permission
from django.db.models import QuerySet
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
        perm: QuerySet[Permission] = Permission.objects.all()[:2]

        if not self.role.permissions.count():
            self.role.permissions.add(perm[0], perm[1])

        self.default_values: DefaultValuesType = {
            "name": "Role2",
            "permissions_ids": [PermissionType.encode_id("PermissionType", str(perm[0].id)),
                                PermissionType.encode_id("PermissionType", str(perm[1].id))]
        }

    async def test_validate_and_get_errors_name(self) -> None:
        input_repeated_name = RoleCreateInput(name=self.role.name,
                                              permissions_ids=self.default_values["permissions_ids"])
        name_error_payload: List[UserError] = await input_repeated_name.validate_and_get_errors()
        self.assertIsInstance(name_error_payload[0], CannotCreateRoleNameIsNotUnique)

    async def test_validate_and_get_errors_perm(self) -> None:
        last_perm = await Permission.objects.order_by("id").alast()
        not_existent_id = str(last_perm.id + 1)
        input_non_existent_perm = RoleCreateInput(name=self.default_values["name"],
                                                  permissions_ids=[
                                                      PermissionType.encode_id("PermissionType", not_existent_id)])
        perm_error_payload: List[UserError] = await input_non_existent_perm.validate_and_get_errors()
        self.assertIsInstance(perm_error_payload[0], CannotCreateRolePermissionDoesNotExist)

    async def test_validate_and_get_errors_all(self) -> None:
        last_perm = await Permission.objects.order_by("id").alast()
        not_existent_id = str(last_perm.id + 1)
        all_error_input = RoleCreateInput(name=self.role.name,
                                          permissions_ids=[PermissionType.encode_id("PermissionType", not_existent_id)])
        all_error_payload: List[UserError] = await all_error_input.validate_and_get_errors()
        self.assertIsInstance(all_error_payload[0], CannotCreateRoleNameIsNotUnique)
        self.assertIsInstance(all_error_payload[1], CannotCreateRolePermissionDoesNotExist)

    async def test_validate_and_get_errors_no_errors(self) -> None:
        role_create_input = RoleCreateInput(**self.default_values)
        expected_no_errors = await role_create_input.validate_and_get_errors()
        self.assertFalse(expected_no_errors)
