from strawberry.types import Info
from strawberry_django_plus import gql

from inventory.api.types.stock_recount_document_type.stock_recount_document_input import StockRecountDocumentCreateInput
from inventory.api.types.stock_recount_document_type.stock_recount_document_type import StockRecountDocumentType
from inventory.models import StockRecountDocument, StockMovementAction


@gql.django.mutation
async def stock_recount_document_create(self, info: Info,
                                        input: StockRecountDocumentCreateInput) -> StockRecountDocumentType:
    # Create a new StockRecountDocument object with the given warehouse ID and description
    created_document = await StockRecountDocument.objects.acreate(
        warehouse_id=input.warehouse.id.node_id,
        description=input.description
    )

    # Create StockMovementAction objects for each stock_movement in the input
    movement_actions = []
    for movement in input.stock_movements:
        # Create a new StockMovementAction object with the relevant fields
        movement_action = await StockMovementAction.objects.acreate(
            item_id=movement.item.id.node_id,  # ID of the item involved in the movement
            parent_document=created_document,
            modification_amount=movement.modification_amount,
            description=movement.description,
            is_cumulative=False
            # Indicates if the modification is cumulative, if not the value will be overriden
        )
        # Add the created StockMovementAction to the list of movement actions
        movement_actions.append(movement_action)

    # Set the created movement actions for the stock_movements field of the created_document
    await created_document.stock_movements.aset(movement_actions)

    # Return the created_document
    return created_document
