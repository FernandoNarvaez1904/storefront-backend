from typing import cast, TypedDict, List, Optional

from django.contrib.auth.models import Group, Permission
from django.test import TransactionTestCase
from strawberry import ID

from storefront_backend.api.relay.connection import Connection
from users.api.mutations.role_create.role_create_input import RoleCreateInput
from users.api.mutations.role_create.role_create_payload import RoleCreatePayload
from users.api.mutations.role_create.role_create_resolver import role_create_resolver
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType


class RoleCreateInputData(TypedDict):
    name: str
    permissions_ids: Optional[List[ID]]


class TestRoleCreateResolver(TransactionTestCase):

    def setUp(self) -> None:
        perm = Permission.objects.all()
        self.input: RoleCreateInputData = {
            "name": "Role1",
            "permissions_ids": [PermissionType.encode_id("PermissionType", str(perm[0].id)),
                                PermissionType.encode_id("PermissionType", str(perm[1].id))]

        }

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

    async def test_role_create_resolver_side_effect(self):
        # Building input
        role_create_input = RoleCreateInput(**self.input)

        # Creating user
        await role_create_resolver(input=role_create_input)

        # Checking if field was updated in database
        does_role_exist = await Group.objects.filter(name=self.input["name"]).aexists()
        self.assertTrue(does_role_exist)
