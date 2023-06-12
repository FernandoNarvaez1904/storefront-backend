from abc import ABC

from strawberry_django_plus import gql

from company.models import PaymentMethod


@gql.django.type(PaymentMethod)
class PaymentMethodType(gql.relay.Node, ABC):
    name: str
