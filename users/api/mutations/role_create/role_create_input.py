from typing import List, cast

import strawberry
from django.contrib.auth.models import Permission
from strawberry import ID

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.types import InputTypeInterface, UserError
from users.api.mutations.role_create.role_create_errors import CannotCreateRoleNameIsNotUnique, \
    CannotCreateRolePermissionDoesNotExist
from users.api.types.role_type import RoleType
from users.models import Role


@strawberry.input
class RoleCreateInput(InputTypeInterface):
    name: str
    permissions_ids: List[ID]

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []

        if await Role.objects.filter(name=self.name).aexists():
            errors.append(CannotCreateRoleNameIsNotUnique(
                message="Name already exist, please try with another one"
            ))

        if self.permissions_ids:

            ids: List[int] = []
            is_perm_id = True
            for i in self.permissions_ids:
                decoded_id: DecodedID = RoleType.decode_id(i)

                if not decoded_id["type_name"] == "PermissionType":
                    is_perm_id = False
                    break

                instance_id: str = cast(str, decoded_id["instance_id"])
                ids.append(int(instance_id))

            perms = await Permission.objects.filter(id__in=ids).acount()

            if not perms == len(self.permissions_ids) or not is_perm_id:
                errors.append(
                    CannotCreateRolePermissionDoesNotExist(
                        message=f"Some of the permission_ids given are incorrect or does not represent a Permission"
                    ))

        return errors
