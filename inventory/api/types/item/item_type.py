from abc import ABC
from datetime import datetime
from typing import Optional

from asgiref.sync import sync_to_async
from strawberry import auto
from strawberry_django_plus import gql
from strawberry_django_plus.relay import GlobalID

from inventory.models import Item, ItemDetail


@gql.django.type(ItemDetail)
class ItemVersionType(gql.Node, ABC):
    id: auto
    name: auto
    barcode: auto
    cost: auto
    markup: auto


@gql.django.type(model=Item)
class ItemType(gql.relay.Node, ABC):
    id: auto
    is_active: auto
    current_stock: auto
    is_service: auto
    sku: auto
    item_versions: gql.relay.Connection["ItemVersionType"] = gql.relay.connection()

    @gql.django.field
    async def name(self: Item) -> Optional[str]:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            return detail.name
        except AttributeError:
            return None

    @gql.django.field
    async def barcode(self: Item) -> Optional[str]:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            return detail.barcode
        except AttributeError:
            return None

    @gql.django.field
    async def cost(self: Item) -> float:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            return detail.cost
        except AttributeError:
            return 0

    @gql.django.field
    async def markup(self: Item) -> float:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            return detail.markup
        except AttributeError:
            return 0

    @gql.django.field
    async def creation_date(self: Item) -> Optional[datetime]:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            return detail.date
        except AttributeError:
            return None

    @gql.django.field
    async def price(self: Item) -> Optional[float]:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            cost = detail.cost
            return cost + (cost * (detail.markup / 100))
        except AttributeError:
            return None

    @gql.django.field
    async def version_id(self: Item) -> Optional[GlobalID]:
        try:
            pk = self.current_detail_id
            detail: ItemDetail = await sync_to_async(ItemDetail.objects.get)(pk=pk)
            return GlobalID(node_id=f"{detail.id}", type_name="ItemVersionType")
        except AttributeError:
            return None
