from typing import cast, TypedDict, List, Optional

from django.contrib.auth.models import Permission
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
from users.api.mutations.role_add_permission.role_add_permission_payload import RoleAddPermissionPayload
from users.api.mutations.role_add_permission.role_add_permission_resolver import role_add_permission_resolver
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType
from users.models import Role, User


class DefaultValuesType(TypedDict):
    role_id: ID
    permissions_ids: List[ID]


class TestRoleAddPermissionResolver(TransactionTestCase):

    def setUp(self) -> None:
        perm = Permission.objects.all()
        self.role = Role.objects.create(name="Role1")

        self.input: DefaultValuesType = {
            "role_id": RoleType.encode_id(str(self.role.id)),
            "permissions_ids": [
                PermissionType.encode_id(str(perm[0].id)),
                PermissionType.encode_id(str(perm[1].id))
            ]

        }
        self.mutation_query = """
            mutation RoleAddPermission($input: RoleAddPermissionInput!) {
              roleAddPermission(input: $input) {
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
            "roleId": RoleType.encode_id(str(self.role.id)),
            "permissionsIds": [
                PermissionType.encode_id(str(perm[0].id)),
                PermissionType.encode_id(str(perm[1].id))
            ]
        }}

    async def test_role_add_permission_resolver_response(self) -> None:
        role_add_input = RoleAddPermissionInput(**self.input)
        result: RoleAddPermissionPayload = cast(RoleAddPermissionPayload,
                                                await role_add_permission_resolver(input=role_add_input))

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, RoleAddPermissionPayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        node: Optional[RoleType] = result.node
        self.assertIsNotNone(node)
        if node:
            self.assertIsNotNone(node.id)

            # Test returning the two permission added
            permissions: Connection[PermissionType] = await node.permissions()
            returned_perm_ids: List[ID] = [perm.node.id for perm in permissions.edges]

            # test if they are the same size
            self.assertEqual(len(self.input["permissions_ids"]), len(returned_perm_ids))

            # Test if the permission returned are the one passed on the input
            for i in self.input["permissions_ids"]:
                self.assertIn(i, returned_perm_ids)

    async def test_role_add_permission_resolver_side_effect(self) -> None:
        # Building input
        role_create_input = RoleAddPermissionInput(**self.input)

        # Adding permission to role
        await role_add_permission_resolver(input=role_create_input)

        # Getting Role Object
        role_id = RoleType.decode_id(self.input["role_id"])["instance_id"]
        role = await Role.objects.aget(id=role_id)

        role_permissions: List[Permission] = await get_lazy_query_set_as_list(role.permissions.all())

        returned_perm_ids: List[ID] = [await PermissionType.get_id_from_model_instance(perm) for perm in
                                       role_permissions]

        # test if they are the same size
        self.assertEqual(len(self.input["permissions_ids"]), len(returned_perm_ids))

        # Test if the permission returned are the one passed on the input
        for i in self.input["permissions_ids"]:
            self.assertIn(i, returned_perm_ids)

    async def test_role_add_permission_resolver_permission_denied(self) -> None:
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["roleAddPermission"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_role_add_permission_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "add_permission_to_role")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["roleAddPermission"]["userErrors"]
            self.assertFalse(user_errors)
