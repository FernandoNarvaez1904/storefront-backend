from typing import List, TypedDict, cast

from django.contrib.auth.models import Permission
from django.db.models import QuerySet
from django.test import TransactionTestCase
from strawberry import ID

from storefront_backend.api.types import UserError
from users.api.mutations.role_add_permission.role_add_permission_errors import RoleDoesNotExistError, \
    PermissionDoesNotExistError, ListOfIDIsEmptyError
from users.api.mutations.role_add_permission.role_add_permission_input import RoleAddPermissionInput
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType
from users.models import Role


class DefaultValuesType(TypedDict):
    role_id: ID
    permissions_ids: List[ID]


class TestRoleAddPermissionInput(TransactionTestCase):

    def setUp(self) -> None:
        self.role = Role.objects.create(name="Role1")

        perms: QuerySet[Permission] = Permission.objects.all()[:2]
        self.default_values: DefaultValuesType = {
            "role_id": RoleType.encode_id(str(self.role.id)),
            "permissions_ids": [PermissionType.encode_id(str(perms[0].id)),
                                PermissionType.encode_id(str(perms[1].id))]
        }

    async def test_validate_and_get_errors_id(self) -> None:
        last_role = cast(Role, await Role.objects.alast())
        not_valid_id = RoleType.encode_id(str(last_role.id + 1))
        input_not_valid_id = RoleAddPermissionInput(
            role_id=not_valid_id,
            permissions_ids=self.default_values["permissions_ids"]
        )
        id_error_payload: List[UserError] = await input_not_valid_id.validate_and_get_errors()
        self.assertIsInstance(id_error_payload[0], RoleDoesNotExistError)

    async def test_validate_and_get_errors_perm_incorrect(self) -> None:
        last_role = cast(Role, await Role.objects.alast())
        not_existent_perm_id: ID = PermissionType.encode_id(str(last_role.id + 1))
        input_non_existent_perm = RoleAddPermissionInput(
            role_id=self.default_values["role_id"],
            permissions_ids=[not_existent_perm_id]
        )
        perm_error_payload: List[UserError] = await input_non_existent_perm.validate_and_get_errors()
        self.assertIsInstance(perm_error_payload[0], PermissionDoesNotExistError)

    async def test_validate_and_get_errors_perm_empty(self) -> None:
        input_empty_perm = RoleAddPermissionInput(
            role_id=self.default_values["role_id"],
            permissions_ids=[]
        )
        perm_empty_error_payload: List[UserError] = await input_empty_perm.validate_and_get_errors()
        self.assertIsInstance(perm_empty_error_payload[0], ListOfIDIsEmptyError)

    async def test_validate_and_get_errors_all_id_and_perm_incorrect(self) -> None:
        last_role = cast(Role, await Role.objects.alast())
        not_existent_role_id: ID = RoleType.encode_id(str(last_role.id + 1))
        all_id_and_perm_incorrect_input = RoleAddPermissionInput(
            role_id=not_existent_role_id,
            permissions_ids=[PermissionType.encode_id(str(last_role.id + 1))]
        )
        all_id_and_perm_incorrect_payload: List[
            UserError] = await all_id_and_perm_incorrect_input.validate_and_get_errors()
        self.assertIsInstance(all_id_and_perm_incorrect_payload[0], RoleDoesNotExistError)
        self.assertIsInstance(all_id_and_perm_incorrect_payload[1], PermissionDoesNotExistError)

    async def test_validate_and_get_errors_all_id_and_perm_empty(self) -> None:
        last_role = cast(Role, await Role.objects.alast())
        not_existent_role_id: ID = RoleType.encode_id(str(last_role.id + 1))
        all_id_and_perm_empty_input = RoleAddPermissionInput(role_id=not_existent_role_id, permissions_ids=[])
        all_id_and_perm_empty_payload: List[UserError] = await all_id_and_perm_empty_input.validate_and_get_errors()
        self.assertIsInstance(all_id_and_perm_empty_payload[0], RoleDoesNotExistError)
        self.assertIsInstance(all_id_and_perm_empty_payload[1], ListOfIDIsEmptyError)

    async def test_validate_and_get_errors_no_errors(self) -> None:
        role_add_perm_input = RoleAddPermissionInput(**self.default_values)
        expected_no_errors = await role_add_perm_input.validate_and_get_errors()
        self.assertFalse(expected_no_errors)
