from strawberry_django_plus import gql

from inventory.api.types.item_type.item_input import ItemCreateInput, ItemUpdateInput
from inventory.api.types.item_type.item_type import ItemType


@gql.type
class Mutation:
    item_create: ItemType = gql.django.create_mutation(ItemCreateInput)
    item_update: ItemType = gql.django.update_mutation(ItemUpdateInput)
