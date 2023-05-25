from django.db import models

from document_management.models import DocumentInterface
from inventory.models import Item, Warehouse


# Create your models here.
class StockModificationDocument(DocumentInterface):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    modification_amount = models.FloatField()

    @property
    def is_stock_transfer(self) -> bool:
        return bool(self.stock_transfer_received) or bool(self.stock_transfer_send)


class StockTransferDocument(DocumentInterface):
    receiving_warehouse_modified_items = models.ManyToManyField(StockModificationDocument,
                                                                related_name="stock_transfer_received")
    sender_warehouse_modified_items = models.ManyToManyField(StockModificationDocument,
                                                             related_name="stock_transfer_send")
    

class StockRecountDocument(DocumentInterface):
    modified_item_entry = models.ForeignKey(StockModificationDocument, on_delete=models.PROTECT)
