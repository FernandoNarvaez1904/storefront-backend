from typing import Iterable, Optional

from asgiref.sync import sync_to_async
import strawberry

from company.models import PaymentMethod
from company.types.paymeny_method_type.payment_method_filter import PaymentMethodFilter
from company.types.paymeny_method_type.payment_method_type import PaymentMethodType
from storefront_backend.api.utils.filter_connection import get_filter_arg_from_filter_input


@strawberry.relay.connection(strawberry.relay.ListConnection[PaymentMethodType])
async def payment_method_connection(self, filter: Optional[PaymentMethodFilter] = None) -> Iterable[PaymentMethodType]:
    filter_temp = {}
    if filter:
        filter_temp = await get_filter_arg_from_filter_input(filter)

    payment_methods = PaymentMethod.objects.filter(**filter_temp)
    await sync_to_async(len)(payment_methods)
    return payment_methods
