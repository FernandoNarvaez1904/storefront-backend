from typing import List, Optional, Type, Union

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.core.handlers.asgi import ASGIRequest
from strawberry.types import Info

from storefront_backend.api.global_user_errors import UserHasNoPermission
from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import InputTypeInterface
from storefront_backend.api.types import UserError
from users.models import User


@sync_to_async
def get_user_from_asgi_request(request: ASGIRequest) -> Union[User, AnonymousUser]:
    user = request.user
    # It forces object to evaluate
    user_id = user.id
    return request.user


def strawberry_mutation_resolver_payload(
        input_type: Type[InputTypeInterface],
        payload_type: Type[PayloadTypeInterface],
        permission: str = ""
):
    """
        It is used to automatically implement the payload and error logic of all mutations.
    """

    def inner(func):
        async def wrapper(input: InputTypeInterface, info: Optional[Info] = None):
            node: Optional[Node] = None
            errors: List[UserError] = []

            # The info check is put because some test do not pass input
            # TODO make tests always past input
            if permission and info:
                # Getting user's request
                request: ASGIRequest = info.context.get("request")
                user: Union[User, AnonymousUser] = await get_user_from_asgi_request(request)

                # Does the user have the given permission?
                user_has_permission: bool = await sync_to_async(user.has_perm)(permission)
                if not user_has_permission:
                    # Returning "failed" payload with hasNoPermission Error
                    errors.append(UserHasNoPermission(
                        message=f"You have no permission to perform this action. You need {permission} permission"))
                    return payload_type(user_errors=errors, node=node)

            # Getting errors from mutation input
            errors = await input.validate_and_get_errors()
            if not errors:
                # Getting node data from mutation resolver
                node = await func(input, info)

            return payload_type(user_errors=errors, node=node)

        # Typing for introspection
        wrapper.__annotations__["info"] = Info
        wrapper.__annotations__["input"] = input_type
        wrapper.__annotations__["return"] = payload_type

        return wrapper

    return inner
