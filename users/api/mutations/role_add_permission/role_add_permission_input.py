from typing import List, cast

import strawberry
from django.contrib.auth.models import Permission
from strawberry import ID

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.types import InputTypeInterface, UserError
from users.api.types.role_type import RoleType
from users.models import Role
from .role_add_permission_errors import RoleDoesNotExistError, PermissionDoesNotExistError, ListOfIDIsEmptyError
from ...types.permission_type import PermissionType


@strawberry.input
class RoleAddPermissionInput(InputTypeInterface):
    role_id: ID
    permissions_ids: List[ID]

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []

        role_id = RoleType.decode_id(self.role_id)["instance_id"]
        if not await Role.objects.filter(pk=role_id).aexists():
            errors.append(RoleDoesNotExistError(
                message="The id provided does not match with any Role"
            ))

        if self.permissions_ids:

            ids: List[int] = []
            is_perm_id = True
            for i in self.permissions_ids:
                decoded_id: DecodedID = PermissionType.decode_id(i)

                if not decoded_id["type_name"] == "PermissionType":
                    is_perm_id = False
                    break

                instance_id: str = cast(str, decoded_id["instance_id"])
                ids.append(int(instance_id))

            perms = await Permission.objects.filter(id__in=ids).acount()

            if not perms == len(self.permissions_ids) or not is_perm_id:
                errors.append(
                    PermissionDoesNotExistError(
                        message=f"Some of the permission_ids given are incorrect or does not represent a Permission"
                    ))
        else:
            errors.append(
                ListOfIDIsEmptyError(message="permissionIds cannot be empty")
            )

        return errors
