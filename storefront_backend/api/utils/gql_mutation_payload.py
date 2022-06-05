from typing import TypeVar, List, Optional

from strawberry_django_plus import gql

from storefront_backend.api.types import UserError, InputTypeInterface, PayloadTypeInterface

InputType = TypeVar("InputType")
PayloadType = TypeVar("PayloadType")
ReturnedType = TypeVar("ReturnedType")


async def check_if_type_vars_are_correct_instance(input_type: InputType,
                                                  payload_type: PayloadType,
                                                  returned_type: ReturnedType) -> bool:
    if not issubclass(input_type, InputTypeInterface):
        raise TypeError("input_type must be a subclass or instance of InputTypeInterface ")
    if not issubclass(payload_type, PayloadTypeInterface):
        raise TypeError("payload_type must be a subclass or instance of PayloadTypeInterface ")
    if not issubclass(returned_type, gql.Node):
        raise TypeError("returned_type must be a subclass or instance of gql.Node ")

    return True


def gql_mutation_payload(
        input_type: InputType,
        payload_type: PayloadType,
        returned_type: ReturnedType
):
    """
        It is used to automatically implement the payload and error logic of all mutations.
    """

    def inner(func):
        @gql.field
        async def wrapper(self, input: input_type) -> payload_type:
            await check_if_type_vars_are_correct_instance(
                input_type=input_type,
                payload_type=payload_type,
                returned_type=returned_type
            )
            errors: List[UserError] = await input.validate_and_get_errors()
            node: Optional[returned_type] = None
            if not errors:
                node: returned_type = await func(self=self, input=input)
            return payload_type(user_errors=errors, node=node)

        return wrapper

    return inner
