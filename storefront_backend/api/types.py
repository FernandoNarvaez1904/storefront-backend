from typing import List, Optional

import strawberry
from strawberry_django.filters import FilterLookup


@strawberry.interface(description=" It gives the API user a hint on the not allowed inputs or errors in the mutation.")
class UserError:
    field: str
    message: str


@strawberry.interface
class InputTypeInterface:

    async def validate_and_get_errors(self) -> List[UserError]:
        pass


@strawberry.input
class Filter:
    id: Optional[FilterLookup[strawberry.ID]] = strawberry.UNSET
