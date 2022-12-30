from typing import cast, TypedDict, List, Optional

from django.test import TransactionTestCase
from strawberry import ID
from strawberry.django.context import StrawberryDjangoContext
from strawberry.django.views import TemporalHttpResponse
from strawberry.types import ExecutionResult

from storefront_backend.api.relay.connection import Connection
from storefront_backend.api.schema import schema
from storefront_backend.api.utils.filter_connection import get_lazy_query_set_as_list
from storefront_backend.tests.utils import create_user_with_permission, get_async_request_with_user_and_session
from users.api.mutations.role_add_users.role_add_users_input import RoleAddUsersInput
from users.api.mutations.role_add_users.role_add_users_payload import RoleAddUsersPayload
from users.api.mutations.role_add_users.role_add_users_resolver import role_add_users_resolver
from users.api.types.role_type import RoleType
from users.api.types.user_type import UserType
from users.models import Role, User


class DefaultValuesType(TypedDict):
    role_id: ID
    users_ids: List[ID]


class TestRoleAddUsersResolver(TransactionTestCase):

    def setUp(self) -> None:
        self.users: List[User] = [User.objects.create_user(username=f"user{i}", password=f"{i}") for i in range(2)]
        self.role = Role.objects.create(name="Role1")

        self.input: DefaultValuesType = {
            "role_id": RoleType.encode_id(str(self.role.id)),
            "users_ids": [
                UserType.encode_id(str(self.users[0].id)),
                UserType.encode_id(str(self.users[1].id))
            ]

        }
        self.mutation_query = """
            mutation RoleAddUsers($input: RoleAddUsersInput!) {
              roleAddUsers(input: $input) {
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
            "usersIds": [
                UserType.encode_id(str(self.users[0].id)),
                UserType.encode_id(str(self.users[1].id))
            ]
        }}

    async def test_role_add_users_resolver_response(self) -> None:
        role_add_input = RoleAddUsersInput(**self.input)
        result: RoleAddUsersPayload = cast(RoleAddUsersPayload,
                                           await role_add_users_resolver(input=role_add_input))

        # Test if resolver is returning the correct payload
        self.assertIsInstance(result, RoleAddUsersPayload)

        # Test if payload has no errors
        self.assertFalse(result.user_errors)

        # Test if id is not null
        node: Optional[RoleType] = result.node
        self.assertIsNotNone(node)
        if node:
            self.assertIsNotNone(node.id)

            # Test returning the two users added
            users: Connection[UserType] = await node.users()
            returned_user_ids: List[ID] = [user.node.id for user in users.edges]

            # test if they are the same size
            self.assertEqual(len(self.input["users_ids"]), len(returned_user_ids))

            # Test if the users returned are the ones passed on the input
            for i in self.input["users_ids"]:
                self.assertIn(i, returned_user_ids)

    async def test_role_add_users_resolver_side_effect(self) -> None:
        # Building input
        role_add_users_input = RoleAddUsersInput(**self.input)

        # Adding users to role
        await role_add_users_resolver(input=role_add_users_input)

        # Getting Role Object
        role_id = RoleType.decode_id(self.input["role_id"])["instance_id"]
        role = await Role.objects.aget(id=role_id)

        # Retrieve the users assigned to the role
        role_users = await get_lazy_query_set_as_list(role.user_set.all())

        # Encode the IDs of the users assigned to the role
        returned_user_ids = [await UserType.get_id_from_model_instance(user) for user in role_users]

        # Assert that the number of users passed in the input is the same as the number of users returned
        self.assertEqual(len(self.input["users_ids"]), len(returned_user_ids))

        # Assert that all the user IDs passed in the input are present in the list of returned user IDs
        for user_id in self.input["users_ids"]:
            self.assertIn(user_id, returned_user_ids)

    async def test_role_add_users_resolver_permission_denied(self) -> None:
        # create a user without the required `add_role_to_user` permission
        user: User = await create_user_with_permission("User", "Password")
        request = await get_async_request_with_user_and_session(user=user)

        # execute the mutation using the user and request
        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        # check that the response data is not None
        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            # get the user errors from the response data
            user_errors: List[dict] = execution_result.data["roleAddUsers"]["userErrors"]
            # check that the first error has the field "permission"
            self.assertEqual(user_errors[0]["field"], "permission")

    async def test_role_add_users_resolver_permission_accepted(self) -> None:
        # Create a user with the required permission to add users to a role
        user: User = await create_user_with_permission("User", "Password", "add_role_to_user")
        request = await get_async_request_with_user_and_session(user=user)

        # Execute the GraphQL query and get the execution result
        execution_result: ExecutionResult = await schema.execute(
            self.mutation_query,
            self.mutation_variables,
            StrawberryDjangoContext(request, TemporalHttpResponse())
        )

        # Check if data is returned
        self.assertIsNotNone(execution_result.data)
        if execution_result.data:
            # Get the list of user errors returned in the payload
            user_errors: List[dict] = execution_result.data["roleAddUsers"]["userErrors"]
            # Assert that there are no user errors
            self.assertFalse(user_errors)
