from inventory.api.mutations.item_activate.item_activate_errors import CannotActivateAlreadyActiveItem, \
    CannotActivateNonExistentItem
from inventory.api.mutations.item_create.item_create_errors import CannotCreateItemBarcodeIsNotUnique, \
    CannotCreateItemNameIsNotUnique, CannotCreateItemSkuIsNotUnique
from inventory.api.mutations.item_deactivate.item_deactivate_errors import CannotDeactivateInactiveItem, \
    CannotDeactivateNonExistentItem
from inventory.api.mutations.item_delete.item_delete_errors import CannotDeleteItemHasDocuments, \
    CannotDeleteNonExistentItem
from inventory.api.mutations.item_update.item_update_errors import CannotUpdateInactiveItem, \
    CannotUpdateNonExistentItem, CannotUpdateItemBarcodeIsNotUnique, CannotUpdateItemSkuIsNotUnique, CannotUpdateItemNameIsNotUnique

exported_types = [
    # Item Create
    CannotCreateItemBarcodeIsNotUnique,
    CannotCreateItemNameIsNotUnique,
    CannotCreateItemSkuIsNotUnique,

    # Item Delete
    CannotDeleteItemHasDocuments,
    CannotDeleteNonExistentItem,

    # Item Update
    CannotUpdateInactiveItem,
    CannotUpdateNonExistentItem,
    CannotUpdateItemBarcodeIsNotUnique,
    CannotUpdateItemNameIsNotUnique,
    CannotUpdateItemSkuIsNotUnique,

    # Item Activate
    CannotActivateAlreadyActiveItem,
    CannotActivateNonExistentItem,

    # Item Deactivate
    CannotDeactivateInactiveItem,
    CannotDeactivateNonExistentItem
]
