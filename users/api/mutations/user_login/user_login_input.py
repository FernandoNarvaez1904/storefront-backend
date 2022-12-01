from typing import List

import strawberry
from asgiref.sync import sync_to_async

from storefront_backend.api.types import UserError, InputTypeInterface
from users.api.mutations.user_login.user_login_errors import CannotLoginUsernameDoesNotExist, \
    CannotLoginPasswordIsNotCorrect
from users.models import User


@strawberry.input
class UserLoginInput(InputTypeInterface):
    username: str
    password: str

    async def validate_and_get_errors(self) -> List[UserError]:
        errors: List[UserError] = []

        user_filtered = await sync_to_async(list)(User.objects.filter(username=self.username))
        if not user_filtered:
            errors.append(CannotLoginUsernameDoesNotExist(
                message="Username does not exist"
            ))
        else:
            is_password_correct = await sync_to_async(user_filtered[0].check_password)(self.password)
            if not is_password_correct:
                errors.append(CannotLoginPasswordIsNotCorrect(
                    message="Password is not correct"
                ))

        return errors
