from typing import List

from strawberry_django_plus import gql


@gql.interface
class UserError:
    field: str
    message: str


@gql.interface
class Payload:
    user_errors: List[UserError]
