from typing import List

import strawberry

from storefront_backend.api.types import UserError, InputTypeInterface
from users.api.mutations.user_create.user_create_errors import CannotCreateUserUsernameIsNotUnique, \
    CannotCreateUserEmailIsNotUnique
from users.models import User


@strawberry.input
class UserCreateInput(InputTypeInterface):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []

        if await User.objects.filter(username=self.username).aexists():
            errors.append(CannotCreateUserUsernameIsNotUnique(
                message="Username already exist, please try with another one"
            ))

        if await User.objects.filter(email=self.email).aexists():
            errors.append(CannotCreateUserEmailIsNotUnique(
                message="Email already exist, please try with another one"
            ))

        return errors
