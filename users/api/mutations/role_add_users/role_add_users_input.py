from typing import List, cast

import strawberry
from strawberry import ID

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.types import InputTypeInterface, UserError
from users.api.types.role_type import RoleType
from users.models import Role, User
from .role_add_users_errors import UserDoesNotExistError, ListOfIDIsEmptyError, RoleDoesNotExistError
from ...types.user_type import UserType


@strawberry.input
class RoleAddUsersInput(InputTypeInterface):
    role_id: ID
    users_ids: List[ID]

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []

        # Decode the role ID and check if the corresponding role exists
        role_id = RoleType.decode_id(self.role_id)["instance_id"]
        if not await Role.objects.filter(pk=role_id).aexists():
            errors.append(RoleDoesNotExistError(
                message="The id provided does not match with any Role"
            ))

        # If the users_ids field is not empty, validate the user IDs
        if self.users_ids:
            user_ids: List[int] = []
            # Assume that all the user IDs are valid until proven otherwise
            is_user_id = True

            for i in self.users_ids:
                decoded_id: DecodedID = UserType.decode_id(i)

                # If the type name of the decoded ID is not "UserType", mark the user IDs as invalid
                if not decoded_id["type_name"] == "UserType":
                    is_user_id = False
                    break

                # Otherwise, append the instance ID it to the list of user IDs
                instance_id: str = cast(str, decoded_id["instance_id"])
                user_ids.append(int(instance_id))

            # Check if the number of users with an ID in the list of user IDs is equal to the number of users_ids
            # If not, or if any of the user IDs are invalid, append a UserDoesNotExistError to the list of errors
            users = await User.objects.filter(id__in=user_ids).acount()
            if not users == len(self.users_ids) or not is_user_id:
                errors.append(
                    UserDoesNotExistError(
                        message=f"Some of the users_ids given are incorrect or does not represent a User"
                    ))
        # If the users_ids field is empty, append a ListOfIDIsEmptyError to the list of errors
        else:
            errors.append(
                ListOfIDIsEmptyError(message="usersIds cannot be empty")
            )

        return errors
