from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from inventory.models import WarehouseStock, StockMovementAction, Item, Warehouse


# Signal: Triggered after a StockMovementAction object is saved
@receiver(post_save, sender="inventory.StockMovementAction")
def change_stock_count_after_save(sender, instance: "StockMovementAction", *args, **kwargs) -> None:
    """
        This signal updates the stock count of a WarehouseStock object based on the saved StockMovementAction.
        It retrieves or creates a WarehouseStock object associated with the warehouse and item of the StockMovementAction.
        Depending on the is_cumulative attribute of the StockMovementAction, it either adds the modification amount to
        the current stock amount or sets the stock amount to the modification amount. Finally, it saves the WarehouseStock object.
    """

    # Retrieve or create a WarehouseStock object associated with the warehouse and item of the saved StockMovementAction
    ware_stock = WarehouseStock.objects.get_or_create(
        warehouse=instance.parent_document.warehouse, item=instance.item
    )[0]

    # Update the stock_amount based on the modification amount of the StockMovementAction
    if instance.is_cumulative:
        # If is_cumulative is True, add the modification_amount to the current stock_amount
        ware_stock.stock_amount = ware_stock.stock_amount + instance.modification_amount
    else:
        # If is_cumulative is False, set the stock_amount to the modification_amount
        ware_stock.stock_amount = instance.modification_amount

    # Save the updated WarehouseStock object
    ware_stock.save()


# Signal: Triggered before a StockMovementAction object is saved
@receiver(pre_save, sender=StockMovementAction)
def populate_fields_from_item(sender, instance: StockMovementAction, *args, **kwargs) -> None:
    """
        This signal populates various fields of a StockMovementAction object based on the associated item object.
        It sets the item_cost, item_markup, and item_price fields to the corresponding attributes of the item.
        It calculates the modification_cost_value and modification_price_value fields by multiplying the item_cost and
        item_price with the modification_amount, respectively. It also sets the creation_date field to the creation_date
        of the parent document of the StockMovementAction.
    """
    # Populate various fields of the StockMovementAction object based on the associated item object
    instance.item_cost = instance.item.cost
    instance.item_markup = instance.item.markup
    instance.item_price = instance.item.price_c
    instance.creation_date = instance.parent_document.creation_date


# Signal: Triggered after an Item object is saved
@receiver(post_save, sender="inventory.Item")
def add_new_item_to_warehouses_stock(sender, instance: "Item", *args, **kwargs) -> None:
    """
        This signal adds a newly created Item to the stock of all warehouses if it doesn't already exist.
        It checks if the item exists in any warehouses' stock. If not, it retrieves all warehouses and creates
        WarehouseStock objects for the item with an initial stock_amount of 0 for each warehouse.
        The WarehouseStock objects are then bulk created in a single database query.
    """
    # Check if the item already exists in any warehouses' stock
    already_exists_in_warehouses = instance.stock.all().exists()
    if not already_exists_in_warehouses:
        # Retrieve all warehouses
        warehouses = Warehouse.objects.all()

        # Create WarehouseStock objects with the item, respective warehouses, and an initial stock_amount of 0
        warehouses_stock = [
            WarehouseStock(item=instance, warehouse=warehouse, stock_amount=0)
            for warehouse in warehouses
        ]

        # Bulk create the WarehouseStock objects in a single database query
        WarehouseStock.objects.bulk_create(warehouses_stock)


# Signal: Triggered after a Warehouse object is saved
@receiver(post_save, sender="inventory.Warehouse")
def add_items_stock_to_new_warehouse(sender, instance: "Warehouse", *args, **kwargs) -> None:
    """
        This signal adds the stock of all existing items to a newly created Warehouse if it doesn't already have stock.
        It checks if the warehouse has any items in its stock. If not, it retrieves all items and creates WarehouseStock
        objects for each item with an initial stock_amount of 0 for the new warehouse.
        The WarehouseStock objects are then bulk created in a single database query.
    """
    # Check if the warehouse already has any items in its stock
    already_has_stock = instance.stock.all().exists()
    if not already_has_stock:
        # Retrieve all items
        items = Item.objects.all()

        # Create WarehouseStock objects with the items, the warehouse, and an initial stock_amount of 0 for each item
        warehouses_stock = [
            WarehouseStock(item=item, warehouse=instance, stock_amount=0)
            for item in items
        ]

        # Bulk create the WarehouseStock objects in a single database query
        WarehouseStock.objects.bulk_create(warehouses_stock)
