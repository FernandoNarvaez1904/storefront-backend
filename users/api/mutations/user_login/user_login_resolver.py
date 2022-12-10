from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login
from strawberry.types import Info

from storefront_backend.api.utils.strawberry_mutation_resolver_payload import strawberry_mutation_resolver_payload
from users.api.mutations.user_login.user_login_input import UserLoginInput
from users.api.mutations.user_login.user_login_payload import UserLoginPayload
from users.api.types.user_type import UserType


@strawberry_mutation_resolver_payload(
    input_type=UserLoginInput,
    payload_type=UserLoginPayload,
)
async def user_login_resolver(input: UserLoginInput, info: Info) -> UserType:
    request = info.context.get("request")

    # It does not need to check if its valid because the input did that
    user = await sync_to_async(authenticate)(request, username=input.username, password=input.password)
    # It logs the user in by setting a cookie with the sessionid
    await sync_to_async(login)(request, user)

    return await UserType.from_model_instance(user)
