from typing import List

from strawberry_django_plus import gql


@gql.interface(description=" It gives the API user a hint on the not allowed inputs or errors in the mutation.")
class UserError:
    field: str
    message: str


@gql.interface
class Payload:
    user_errors: List[UserError]
