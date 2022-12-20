from typing import cast, TypedDict, List, Optional

from django.contrib.auth.models import Permission
from django.db.models import QuerySet
from django.test import TransactionTestCase
from strawberry import ID
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from storefront_backend.api.relay.connection import Connection
from storefront_backend.api.schema import schema
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list
from storefront_backend.tests.utils import create_user_with_permission, get_async_request_with_user_and_session
from users.api.mutations.role_add_permission.role_add_permission_input import RoleAddPermissionInput
from users.api.mutations.role_remove_permission.role_remove_permission_input import RoleRemovePermissionInput
from users.api.mutations.role_remove_permission.role_remove_permission_payload import RoleRemovePermissionPayload
from users.api.mutations.role_remove_permission.role_remove_permission_resolver import role_remove_permission_resolver
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType
from users.models import Role, User


class DefaultValuesType(TypedDict):
    role_id: ID
    permissions_ids: List[ID]


class TestRoleRemovePermissionResolver(TransactionTestCase):

    def setUp(self) -> None:
        perm: QuerySet[Permission] = Permission.objects.all()[:2]
        self.role = Role.objects.create(name="Role1")
        self.role.permissions.add(perm[0].id, perm[1].id)

        self.input: DefaultValuesType = {
            "role_id": RoleType.encode_id("RoleType", str(self.role.id)),
            "permissions_ids": [
                PermissionType.encode_id("PermissionType", str(perm[0].id)),
                PermissionType.encode_id("PermissionType", str(perm[1].id))
            ]

        }
        self.mutation_query = """
            mutation RoleRemovePermission($input: RoleRemovePermissionInput!) {
              roleRemovePermission(input: $input) {
                node {
                  id
                }
                userErrors {
                  field
                  message
                }
              }
            }
        """
        self.mutation_variables = {"input": {
            "roleId": RoleType.encode_id("RoleType", str(self.role.id)),
            "permissionsIds": [
                PermissionType.encode_id("PermissionType", str(perm[0].id)),
                PermissionType.encode_id("PermissionType", str(perm[1].id))
            ]
        }}

    async def test_role_remove_permission_resolver_response(self) -> None:
        role_remove_input = RoleRemovePermissionInput(**self.input)
        result: RoleRemovePermissionPayload = cast(RoleRemovePermissionPayload,
                                                   await role_remove_permission_resolver(input=role_remove_input))

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, RoleRemovePermissionPayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        node: Optional[RoleType] = result.node
        self.assertIsNotNone(node)
        if node:
            self.assertIsNotNone(node.id)

            # Test returning the two permission added
            permissions: Connection[PermissionType] = await node.permissions()

            # Test if both permissions were discarded
            self.assertFalse(permissions.edges)

    async def test_role_remove_permission_resolver_side_effect(self) -> None:
        # Building input
        role_remove_input = RoleAddPermissionInput(**self.input)

        # Removing permission
        await role_remove_permission_resolver(input=role_remove_input)

        # Getting Role Object
        role_id = RoleType.decode_id(self.input["role_id"])["instance_id"]
        role = await Role.objects.aget(id=role_id)

        role_permissions: List[Permission] = await get_lazy_query_set_as_list(role.permissions.all())

        # Test if both permissions were discarded
        self.assertFalse(role_permissions)

    async def test_remove_create_resolver_permission_denied(self) -> None:
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["roleRemovePermission"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_role_create_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "remove_permission_to_role")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["roleRemovePermission"]["userErrors"]
            self.assertFalse(user_errors)
