from typing import cast, TypedDict, List, Optional

from django.contrib.auth.models import Permission
from django.test import TransactionTestCase
from strawberry import ID
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from storefront_backend.api.relay.connection import Connection
from storefront_backend.api.schema import schema
from storefront_backend.tests.utils import create_user_with_permission, get_async_request_with_user_and_session
from users.api.mutations.role_create.role_create_input import RoleCreateInput
from users.api.mutations.role_create.role_create_payload import RoleCreatePayload
from users.api.mutations.role_create.role_create_resolver import role_create_resolver
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType
from users.models import User, Role


class RoleCreateInputData(TypedDict):
    name: str
    permissions_ids: List[ID]


class TestRoleCreateResolver(TransactionTestCase):

    def setUp(self) -> None:
        perm = Permission.objects.all()
        self.input: RoleCreateInputData = {
            "name": "Role1",
            "permissions_ids": [PermissionType.encode_id(str(perm[0].id)),
                                PermissionType.encode_id(str(perm[1].id))]

        }
        self.mutation_query = """
            mutation RoleCreate($input: RoleCreateInput!) {
              roleCreate(input: $input) {
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
            "name": "Role1",
            "permissionsIds": [PermissionType.encode_id(str(perm[0].id)),
                               PermissionType.encode_id(str(perm[1].id))]

        }}

    async def test_role_create_resolver_response(self) -> None:
        permissions_ids: List[ID] = cast(List[ID], self.input["permissions_ids"])
        role_create_input = RoleCreateInput(name=self.input["name"], permissions_ids=permissions_ids)
        result: RoleCreatePayload = cast(RoleCreatePayload, await role_create_resolver(input=role_create_input))

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, RoleCreatePayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        node: Optional[RoleType] = result.node
        self.assertIsNotNone(node)
        if node:
            self.assertIsNotNone(node.id)

            # Test returning the two permission added
            permissions: Connection[PermissionType] = await node.permissions()
            self.assertEqual(permissions.total_count, len(permissions_ids))
            self.assertEqual(permissions.page_info.total_count, len(permissions_ids))
            self.assertEqual(len(permissions.edges), len(permissions_ids))

        # Test if response has all input data
        for key, value in self.input.items():
            if key == "permissions_ids":
                continue
            self.assertEqual(value, result.node.__getattribute__(key))

    async def test_role_create_resolver_side_effect(self) -> None:

        # Building input
        role_create_input = RoleCreateInput(**self.input)

        # Creating role
        await role_create_resolver(input=role_create_input)

        # Checking if field was updated in database
        does_role_exist = await Role.objects.filter(name=self.input["name"]).aexists()
        self.assertTrue(does_role_exist)

    async def test_role_create_resolver_permission_denied(self) -> None:
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["roleCreate"]["userErrors"]
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_role_create_resolver_permission_accepted(self) -> None:
        user: User = await create_user_with_permission("User", "Password", "add_role")
        request = await get_async_request_with_user_and_session(user=user)

        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            user_errors: List[dict] = execution_result.data["roleCreate"]["userErrors"]
            self.assertFalse(user_errors)
