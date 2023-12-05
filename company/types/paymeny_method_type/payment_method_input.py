from typing import Optional

import strawberry
from strawberry_django import NodeInput

from company.models import PaymentMethod


@strawberry.django.input(PaymentMethod)
class PaymentMethodCreateInput:
    name: str


@strawberry.django.input(PaymentMethod)
class PaymentMethodUpdateInput(NodeInput):
    name: Optional[str]
