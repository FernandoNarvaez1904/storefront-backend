from typing import List, cast

from asgiref.sync import sync_to_async
from django.contrib.auth.models import Group, Permission

from storefront_backend.api.relay.node import DecodedID
from storefront_backend.api.utils.strawberry_mutation_resolver_payload import strawberry_mutation_resolver_payload
from users.api.mutations.role_create.role_create_input import RoleCreateInput
from users.api.mutations.role_create.role_create_payload import RoleCreatePayload
from users.api.types.permission_type import PermissionType
from users.api.types.role_type import RoleType


@strawberry_mutation_resolver_payload(
    input_type=RoleCreateInput,
    payload_type=RoleCreatePayload,
)
async def role_create_resolver(input: RoleCreateInput, info) -> RoleType:
    role = await Group.objects.acreate(name=input.name)

    permissions: List[PermissionType] = []
    if input.permissions_ids:
        ids: List[int] = []
        for i in input.permissions_ids:
            decoded_id: DecodedID = RoleType.decode_id(i)
            instance_id: str = cast(str, decoded_id["instance_id"])
            ids.append(int(instance_id))

        await sync_to_async(role.permissions.add)(*ids)

        permissions_objects: List[Permission] = await sync_to_async(list)(Permission.objects.filter(id__in=ids))
        permissions = [PermissionType.from_model_instance(instance) for instance in permissions_objects]

    return RoleType.from_model_instance(role)
