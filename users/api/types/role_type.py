from typing import Optional

import strawberry
from django.contrib.auth.models import Permission

from storefront_backend.api.relay.connection import Connection, get_cursor_page_from_queryset, \
    get_connection_from_cursor_page
from storefront_backend.api.relay.node import Node
from users.api.types.permission_type import PermissionType
from users.models import Role


@strawberry.type
class RoleType(Node):
    _model_ = Role
    id: strawberry.ID
    name: str

    @strawberry.field
    async def permissions(self, before: Optional[strawberry.ID] = None,
                          after: Optional[strawberry.ID] = None,
                          first: Optional[int] = None,
                          last: Optional[int] = None) -> Connection[PermissionType]:
        group_id = self.decode_id(self.id)["instance_id"]
        qs = Permission.objects.filter(group__id=group_id)
        page = await get_cursor_page_from_queryset(qs, after, before, first, last)
        connection = await get_connection_from_cursor_page(page, PermissionType, total_count_from_query=True)

        return connection
