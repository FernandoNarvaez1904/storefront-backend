import strawberry

from inventory.api.mutations.item_activate.item_activate_resolver import item_activate_resolver
from inventory.api.mutations.item_create.item_create_resolver import item_create_resolver
from inventory.api.mutations.item_deactivate.item_deactivate_resolver import item_deactivate_resolver
from inventory.api.mutations.item_delete.item_delete_resolver import item_delete_resolver
from inventory.api.mutations.item_update.Item_update_resolver import item_update_resolver


@strawberry.type
class Mutation:
    item_activate = strawberry.field(item_activate_resolver)
    item_deactivate = strawberry.field(item_deactivate_resolver)
    item_create = strawberry.field(item_create_resolver)
    item_delete = strawberry.field(item_delete_resolver)
    item_update = strawberry.field(item_update_resolver)
