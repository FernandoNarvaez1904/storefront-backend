from abc import ABC

import strawberry
from strawberry.relay import Node

from company.models import PaymentMethod


@strawberry.django.type(PaymentMethod)
class PaymentMethodType(Node, ABC):
    name: str
