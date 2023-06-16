from strawberry.types import Info
from strawberry_django import auth
from strawberry_django_plus import gql

from users.api.types.role_type.role_input import RoleCreateInput, RoleUpdateInput
from users.api.types.role_type.role_type import RoleType
from users.api.types.user_type.user_input import UserCreateInput, UserUpdateInput, UserUpdatePasswordInput, \
    UserAddRolesInput
from users.api.types.user_type.user_type import UserType
from users.models import User


@gql.type
class Mutation:
    login: UserType = auth.login()
    logout = auth.logout()
    register: UserType = auth.register(UserCreateInput)
    user_update: UserType = gql.django.update_mutation(UserUpdateInput)
    user_add_roles: UserType = gql.django.update_mutation(UserAddRolesInput)
    role_create: RoleType = gql.django.create_mutation(RoleCreateInput)
    role_update: RoleType = gql.django.update_mutation(RoleUpdateInput)

    @gql.django.mutation
    async def update_password(self, info: Info, input: UserUpdatePasswordInput) -> UserType:
        user_id = input.id.node_id
        user: User = await User.objects.aget(id=user_id)
        user.set_password(input.password)
        await user.asave()
        return user
