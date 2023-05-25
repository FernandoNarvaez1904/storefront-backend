from datetime import datetime
from typing import Optional, List
import strawberry
from sales.models import SaleDocument
from storefront_backend.api.relay.node import Node
from inventory.models import Client
from company.models import PaymentMethod
from stock.models import StockModificationDocument
from inventory.api.types.item import ItemType

@strawberry.type
class StockModificationDocumentType(Node):
    _model_:StockModificationDocument
    id:strawberry.ID
    item:ItemType
    modification_amount:float
    is_stock_transfer:bool

@strawberry.type
class PaymentMethodType(Node):
    _model_:PaymentMethod
    id:strawberry.ID
    name:str

@strawberry.type
class ClientType(Node):
    _model_:Client
    id:strawberry.ID
    first_name:str
    last_name:str
    address:str
    creation_date:datetime

@strawberry.type
class SaleType(Node):
    _model_:SaleDocument
    id:strawberry.ID
    client:ClientType
    price_calculated:float
    is_paid:bool
    payment_method:PaymentMethodType
    sold_items: List[StockModificationDocumentType]