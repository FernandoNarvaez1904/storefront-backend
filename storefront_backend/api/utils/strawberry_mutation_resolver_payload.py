from typing import TypeVar, List, Optional, no_type_check

InputType = TypeVar("InputType")
PayloadType = TypeVar("PayloadType")
ReturnedType = TypeVar("ReturnedType")


# I have disabled Mypy as I could not figure out how to make it work with
# resolution and introspection at the same time
@no_type_check
async def check_if_type_vars_are_correct_instance(input_type: InputType,
                                                  payload_type: PayloadType,
                                                  returned_type: ReturnedType) -> bool:
    from storefront_backend.api.query import Node
    from storefront_backend.api.types import InputTypeInterface
    from storefront_backend.api.payload_interface import PayloadTypeInterface

    if not issubclass(input_type, InputTypeInterface):
        raise TypeError(
            "input_type must be a subclass or instance of InputTypeInterface ")
    if not issubclass(payload_type, PayloadTypeInterface):
        raise TypeError(
            "payload_type must be a subclass or instance of PayloadTypeInterface ")
    if not issubclass(returned_type, Node):
        raise TypeError(
            "returned_type must be a subclass or instance of Node ")

    return True


def strawberry_mutation_resolver_payload(
        input_type: InputType,
        payload_type: PayloadType,
        returned_type: ReturnedType
):
    """
        It is used to automatically implement the payload and error logic of all mutations.
    """

    # I have disabled Mypy as I could not figure out how to make it work with
    # resolution and introspection at the same time
    @no_type_check
    def inner(func) -> payload_type:
        async def wrapper(input: input_type, info=None) -> payload_type:
            await check_if_type_vars_are_correct_instance(
                input_type=input_type,
                payload_type=payload_type,
                returned_type=returned_type
            )
            from storefront_backend.api.types import UserError
            errors: List[UserError] = await input.validate_and_get_errors()
            node: Optional[returned_type] = None
            if not errors:
                node = await func(input=input, info=info)
            return payload_type(user_errors=errors, node=node)

        return wrapper

    return inner
