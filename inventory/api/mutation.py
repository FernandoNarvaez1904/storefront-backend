from strawberry_django_plus import gql

from inventory.api.types.item_category_type.item_category_input import ItemCategoryCreateInput
from inventory.api.types.item_category_type.item_category_type import ItemCategoryType
from inventory.api.types.item_type.item_input import ItemCreateInput, ItemUpdateInput
from inventory.api.types.item_type.item_type import ItemType


@gql.type
class Mutation:
    item_create: ItemType = gql.django.create_mutation(ItemCreateInput)
    item_update: ItemType = gql.django.update_mutation(ItemUpdateInput)

    item_category_create: ItemCategoryType = gql.django.create_mutation(ItemCategoryCreateInput)
