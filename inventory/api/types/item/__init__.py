from .item_type import ItemType
from .user_error_types import SKUNotUniqueError, BarcodeNotUniqueError, ItemNotExistError, ItemIsNotActiveError, \
    ItemIsActiveError, ItemAlreadyHasDocument, NameNotUniqueError

not_in_schema_types = [
    SKUNotUniqueError,
    BarcodeNotUniqueError,
    ItemNotExistError,
    ItemIsNotActiveError,
    ItemIsActiveError,
    ItemAlreadyHasDocument,
    NameNotUniqueError,
]
