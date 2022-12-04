from typing import List, Optional, Type

from strawberry.types import Info

from storefront_backend.api.payload_interface import PayloadTypeInterface
from storefront_backend.api.relay.node import Node
from storefront_backend.api.types import InputTypeInterface
from storefront_backend.api.types import UserError


def strawberry_mutation_resolver_payload(
        input_type: Type[InputTypeInterface],
        payload_type: Type[PayloadTypeInterface],
):
    """
        It is used to automatically implement the payload and error logic of all mutations.
    """

    def inner(func):
        async def wrapper(input: InputTypeInterface, info: Optional[Info] = None):
            errors: List[UserError] = await input.validate_and_get_errors()
            node: Optional[Node] = None
            if not errors:
                node = await func(input, info)

            return payload_type(user_errors=errors, node=node)

        # Typing for introspection
        wrapper.__annotations__["info"] = Info
        wrapper.__annotations__["input"] = input_type
        wrapper.__annotations__["return"] = payload_type

        return wrapper

    return inner
