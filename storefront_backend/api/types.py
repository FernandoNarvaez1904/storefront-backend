from typing import List, Optional

from strawberry_django_plus import gql


@gql.interface(description=" It gives the API user a hint on the not allowed inputs or errors in the mutation.")
class UserError:
    field: str
    message: str


@gql.interface
class PayloadTypeInterface:
    user_errors: List[UserError]
    node: Optional[gql.Node]


@gql.interface
class InputTypeInterface:

    async def validate_and_get_errors(self) -> List[UserError]:
        pass
