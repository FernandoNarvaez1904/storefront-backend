from strawberry_django_plus import gql

from inventory.mutations.stock_recount_document_mutations import stock_recount_document_create
from inventory.types.item_category_type.item_category_input import ItemCategoryCreateInput, ItemCategoryUpdateInput
from inventory.types.item_category_type.item_category_type import ItemCategoryType
from inventory.types.item_type.item_input import ItemCreateInput, ItemUpdateInput
from inventory.types.item_type.item_type import ItemType
from inventory.types.warehouse_type.warehouse_input import WarehouseCreateInput, WarehouseUpdateInput
from inventory.types.warehouse_type.warehouse_type import WarehouseType


@gql.type
class Mutation:
    item_create: ItemType = gql.django.create_mutation(ItemCreateInput)
    item_update: ItemType = gql.django.update_mutation(ItemUpdateInput)

    item_category_create: ItemCategoryType = gql.django.create_mutation(ItemCategoryCreateInput)
    item_category_update: ItemCategoryType = gql.django.update_mutation(ItemCategoryUpdateInput)

    warehouse_create: WarehouseType = gql.django.create_mutation(WarehouseCreateInput)
    warehouse_update: WarehouseType = gql.django.update_mutation(WarehouseUpdateInput)

    stock_recount_document_create = stock_recount_document_create
