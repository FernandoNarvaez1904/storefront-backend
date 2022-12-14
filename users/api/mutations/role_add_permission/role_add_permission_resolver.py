from typing import List, cast

from asgiref.sync import sync_to_async

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.utils import strawberry_mutation_resolver_payload
from users.api.mutations.role_add_permission.role_add_permission_input import RoleAddPermissionInput
from users.api.mutations.role_add_permission.role_add_permission_payload import RoleAddPermissionPayload
from users.api.types.role_type import RoleType
from users.models import Role


@strawberry_mutation_resolver_payload(
    input_type=RoleAddPermissionInput,
    payload_type=RoleAddPermissionPayload,
    permission="users.add_permission_to_role"
)
async def role_add_permission_resolver(input: RoleAddPermissionInput, info) -> RoleType:
    role_id = RoleType.decode_id(input.role_id)["instance_id"]
    role = await Role.objects.aget(id=role_id)

    permissions_ids: List[int] = []
    for i in input.permissions_ids:
        decoded_id: DecodedID = RoleType.decode_id(i)
        instance_id: str = cast(str, decoded_id["instance_id"])
        permissions_ids.append(int(instance_id))

    await sync_to_async(role.permissions.add)(*permissions_ids)

    return await RoleType.from_model_instance(role)
