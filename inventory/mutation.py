import strawberry

from strawberry_django import mutations

from inventory.mutations.stock_recount_document_mutations import stock_recount_document_create
from inventory.types.item_category_type.item_category_input import ItemCategoryCreateInput, ItemCategoryUpdateInput
from inventory.types.item_category_type.item_category_type import ItemCategoryType
from inventory.types.item_type.item_input import ItemCreateInput, ItemUpdateInput
from inventory.types.item_type.item_type import ItemType
from inventory.types.warehouse_type.warehouse_input import WarehouseCreateInput, WarehouseUpdateInput
from inventory.types.warehouse_type.warehouse_type import WarehouseType


@strawberry.type
class Mutation:
    item_create: ItemType = mutations.create(ItemCreateInput)
    item_update: ItemType = mutations.update(ItemUpdateInput)

    item_category_create: ItemCategoryType = mutations.create(ItemCategoryCreateInput)
    item_category_update: ItemCategoryType = mutations.update(ItemCategoryUpdateInput)

    warehouse_create: WarehouseType = mutations.create(WarehouseCreateInput)
    warehouse_update: WarehouseType = mutations.update(WarehouseUpdateInput)

    stock_recount_document_create = stock_recount_document_create
