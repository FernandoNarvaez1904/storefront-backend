from typing import cast, Dict

from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from strawberry.types import Info
import strawberry

from company.models import Payment
from inventory.models import StockMovementAction, Item
from sales.models import SaleDocument
from sales.types.sale_document_type.sale_document_input import SaleDocumentCreateInput
from sales.types.sale_document_type.sale_document_type import SaleDocumentType


@strawberry.django.mutation
async def sale_document_create(self, info: Info, input: SaleDocumentCreateInput) -> SaleDocumentType:
    # Validate if all stock_movement is greater than 0
    for mov in input.stock_movements:

        if mov.modification_amount <= 0.00:
            raise ValidationError(
                f"It is not possible to have a negative sale. {mov.item.id}: {mov.modification_amount}"
            )

    # Extract item modifications as (node_id, modification_amount) tuples
    item_modifications = [(movement.item.id.node_id, movement.modification_amount) for movement in
                          input.stock_movements]

    # Extract item IDs from the modifications
    item_ids = [modification[0] for modification in item_modifications]

    # Retrieve the queryset of items from the database based on the item IDs
    items_queryset = Item.objects.filter(id__in=item_ids)

    # Force resolution of items_queryset
    await sync_to_async(len)(items_queryset)

    # Create a dictionary mapping item IDs to Item objects
    item_dict: Dict[str, Item] = {f"{item.id}": item for item in items_queryset}

    # Calculate the sale_total by summing the product of each item's price and its modification amount
    sale_total = sum([item_dict.get(modification[0]).price_c * modification[1] for modification in item_modifications])

    # Calculate the total amount of payments from input.payments
    payment_total = sum(payment.amount for payment in input.payments)

    # Validate if payments are sufficient to realize the sale
    if payment_total != sale_total:
        raise ValidationError(
            f"The payments given sale_total ({payment_total}) are not equal to the sale_total of the items to be sold ({sale_total})")

    sale_document: SaleDocument = await SaleDocument.objects.acreate(
        warehouse_id=input.warehouse.id.node_id,
        description=input.description or None,
        client_id=input.client.id.node_id,
        total=sale_total
    )

    movement_actions = [
        await StockMovementAction.objects.acreate(
            parent_document=sale_document,
            item_id=movement.item.id.node_id,
            modification_amount=-abs(movement.modification_amount),
            description=movement.description,
        ) for movement in input.stock_movements
    ]

    payments = [
        await Payment.objects.acreate(
            amount=payment.amount,
            document=sale_document,
            payment_method_id=payment.payment_method.id.node_id
        )
        for payment in input.payments
    ]

    await sale_document.stock_movements.aset(movement_actions)
    await sale_document.payments.aset(payments)

    return cast(SaleDocumentType, sale_document)
