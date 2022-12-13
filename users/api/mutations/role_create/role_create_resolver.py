from typing import List, cast

from asgiref.sync import sync_to_async
from django.contrib.auth.models import Group

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.utils.strawberry_mutation_resolver_payload import strawberry_mutation_resolver_payload
from users.api.mutations.role_create.role_create_input import RoleCreateInput
from users.api.mutations.role_create.role_create_payload import RoleCreatePayload
from users.api.types.role_type import RoleType


@strawberry_mutation_resolver_payload(
    input_type=RoleCreateInput,
    payload_type=RoleCreatePayload,
    permission="auth.add_group"
)
async def role_create_resolver(input: RoleCreateInput, info) -> RoleType:
    role = await Group.objects.acreate(name=input.name)

    if input.permissions_ids:
        ids: List[int] = []
        for i in input.permissions_ids:
            decoded_id: DecodedID = RoleType.decode_id(i)
            instance_id: str = cast(str, decoded_id["instance_id"])
            ids.append(int(instance_id))

        await sync_to_async(role.permissions.add)(*ids)

    return await RoleType.from_model_instance(role)
