from typing import List, TypedDict, cast

from django.test import TransactionTestCase
from strawberry import ID

from storefront_backend.api.types import UserError
from users.api.mutations.role_remove_users.role_remove_users_errors import RoleDoesNotExistError, UserDoesNotExistError, \
    ListOfIDIsEmptyError
from users.api.mutations.role_remove_users.role_remove_users_input import RoleRemoveUsersInput
from users.api.types.role_type import RoleType
from users.api.types.user_type import UserType
from users.models import Role, User


class DefaultValuesType(TypedDict):
    role_id: ID
    users_ids: List[ID]


class TestRoleRemoveUsersInput(TransactionTestCase):

    def setUp(self) -> None:
        self.role = Role.objects.create(name="Role1")
        self.users: List[User] = [User.objects.create_user(username=f"user{i}", password=f"{i}") for i in range(2)]
        self.role.user_set.add(*self.users)
        self.valid_input_values: DefaultValuesType = {
            "role_id": RoleType.encode_id(str(self.role.id)),
            "users_ids": [UserType.encode_id(str(user.id)) for user in self.users]
        }

    async def test_validate_and_get_errors_with_invalid_role_id(self) -> None:
        # Create an ID for a non-existent role by incrementing the ID of the last role object
        last_role = cast(Role, await Role.objects.alast())
        invalid_role_id = RoleType.encode_id(str(last_role.id + 1))

        # Create an instance of RoleAddUsersInput with the invalid role ID and a list of valid user IDs
        input_with_invalid_role_id = RoleRemoveUsersInput(
            role_id=invalid_role_id,
            users_ids=self.valid_input_values["users_ids"]
        )

        # Call validate_and_get_errors on the input instance and assert that the first element of the returned list
        # is an instance of RoleDoesNotExistError
        error_payload: List[UserError] = await input_with_invalid_role_id.validate_and_get_errors()
        self.assertIsInstance(error_payload[0], RoleDoesNotExistError)

    async def test_validate_and_get_errors_with_invalid_user_id(self) -> None:
        # Create an ID for a non-existent user by incrementing the ID of the last user object
        last_user = cast(User, await User.objects.alast())
        invalid_user_id = UserType.encode_id(str(last_user.id + 1))

        # Create an instance of RoleAddUsersInput with a valid role ID and the invalid user ID
        input_with_invalid_user_id = RoleRemoveUsersInput(
            role_id=self.valid_input_values["role_id"],
            users_ids=[invalid_user_id]
        )

        # Call validate_and_get_errors on the input instance and assert that the first element of the returned list
        # is an instance of UserDoesNotExistError
        error_payload: List[UserError] = await input_with_invalid_user_id.validate_and_get_errors()
        self.assertIsInstance(error_payload[0], UserDoesNotExistError)

    async def test_validate_and_get_errors_with_empty_list_of_user_ids(self) -> None:
        # Create an instance of RoleAddUsersInput with a valid role ID and an empty list of user IDs
        input_with_empty_list_of_user_ids = RoleRemoveUsersInput(
            role_id=self.valid_input_values["role_id"],
            users_ids=[]
        )

        # Call validate_and_get_errors on the input instance and assert that the first element of the returned list
        # is an instance of ListOfIDIsEmptyError
        error_payload: List[UserError] = await input_with_empty_list_of_user_ids.validate_and_get_errors()
        self.assertIsInstance(error_payload[0], ListOfIDIsEmptyError)

    async def test_validate_and_get_errors_with_invalid_role_and_user_ids(self) -> None:
        # Create IDs for non-existent role and user by incrementing the IDs of the last role and user objects
        last_role = cast(Role, await Role.objects.alast())
        invalid_role_id = RoleType.encode_id(str(last_role.id + 1))
        last_user = cast(User, await User.objects.alast())
        invalid_user_id = UserType.encode_id(str(last_user.id + 1))

        # Create an instance of RoleAddUsersInput with the invalid role and user IDs
        input_with_invalid_role_and_user_ids = RoleRemoveUsersInput(
            role_id=invalid_role_id,
            users_ids=[invalid_user_id]
        )

        # Call validate_and_get_errors on the input instance and assert that the first element of the returned list
        # is an instance of RoleDoesNotExistError and the second element is an instance of UserDoesNotExistError
        error_payload: List[UserError] = await input_with_invalid_role_and_user_ids.validate_and_get_errors()
        self.assertIsInstance(error_payload[0], RoleDoesNotExistError)
        self.assertIsInstance(error_payload[1], UserDoesNotExistError)

    async def test_validate_and_get_errors_with_invalid_role_id_and_empty_list_of_user_ids(self) -> None:
        # Create an ID for a non-existent role by incrementing the ID of the last role object
        last_role = cast(Role, await Role.objects.alast())
        invalid_role_id = RoleType.encode_id(str(last_role.id + 1))

        # Create an instance of RoleAddUsersInput with the invalid role ID and an empty list of user IDs
        input_with_invalid_role_id_and_empty_list_of_user_ids = RoleRemoveUsersInput(
            role_id=invalid_role_id,
            users_ids=[]
        )

        # Call validate_and_get_errors on the input instance and assert that the first element of the returned list
        # is an instance of RoleDoesNotExistError and the second element is an instance of ListOfIDIsEmptyError
        error_payload: List[
            UserError] = await input_with_invalid_role_id_and_empty_list_of_user_ids.validate_and_get_errors()
        self.assertIsInstance(error_payload[0], RoleDoesNotExistError)
        self.assertIsInstance(error_payload[1], ListOfIDIsEmptyError)

    async def test_validate_and_get_errors_no_errors(self) -> None:
        role_add_perm_input = RoleRemoveUsersInput(**self.valid_input_values)
        expected_no_errors = await role_add_perm_input.validate_and_get_errors()
        self.assertEqual(expected_no_errors, [])
