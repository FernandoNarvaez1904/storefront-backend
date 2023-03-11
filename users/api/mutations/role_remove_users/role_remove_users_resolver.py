from typing import List, cast

from asgiref.sync import sync_to_async

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.utils import strawberry_mutation_resolver_payload
from users.api.mutations.role_remove_users.role_remove_users_input import RoleRemoveUsersInput
from users.api.mutations.role_remove_users.role_remove_users_payload import RoleRemoveUsersPayload
from users.api.types.role_type import RoleType
from users.models import Role


@strawberry_mutation_resolver_payload(
    input_type=RoleRemoveUsersInput,
    payload_type=RoleRemoveUsersPayload,
    permission="users.remove_role_to_user"
)
async def role_remove_users_resolver(input: RoleRemoveUsersInput, info) -> RoleType:
    role_id = RoleType.decode_id(input.role_id)["instance_id"]
    role = await Role.objects.aget(id=role_id)

    users_ids: List[int] = []
    for i in input.users_ids:
        decoded_id: DecodedID = RoleType.decode_id(i)
        instance_id: str = cast(str, decoded_id["instance_id"])
        users_ids.append(int(instance_id))

    await sync_to_async(role.user_set.remove)(*users_ids)

    return await RoleType.from_model_instance(role)
