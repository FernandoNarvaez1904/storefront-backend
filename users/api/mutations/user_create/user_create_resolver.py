from asgiref.sync import sync_to_async

from storefront_backend.api.utils import strawberry_mutation_resolver_payload
from users.api.mutations.user_create.user_create_input import UserCreateInput
from users.api.mutations.user_create.user_create_payload import UserCreatePayload
from users.api.types.user_type import UserType
from users.models import User


@strawberry_mutation_resolver_payload(
    input_type=UserCreateInput,
    payload_type=UserCreatePayload,
    returned_type=UserType
)
async def user_create_resolver(input: UserCreateInput) -> UserType:
    user = await sync_to_async(User.objects.create_user)(**input.__dict__)
    return UserType.from_model_instance(user)
