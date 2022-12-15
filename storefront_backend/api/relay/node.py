from __future__ import annotations

import base64
from typing import ClassVar, Optional, TypedDict, List, cast, TypeVar

import strawberry
from django.db.models import Model
from strawberry import ID
from strawberry.annotation import StrawberryAnnotation
from strawberry.types.types import TypeDefinition
from typing_extensions import Type


class DecodedID(TypedDict):
    type_name: str
    instance_id: ID


A = TypeVar("A", bound="Node")


@strawberry.interface
class Node:
    id: strawberry.ID
    _model_: ClassVar[Type[Model]]

    @classmethod
    def encode_id(cls, type_name: str, node_id: str) -> ID:
        id_ins = f"{type_name}_{node_id}".encode("utf-8")  # format "typeName_id"
        calc_id: strawberry.ID = cast(ID, base64.b64encode(id_ins).decode())
        return calc_id

    @classmethod
    def decode_id(cls, id: strawberry.ID) -> DecodedID:
        bt: bytes = id.encode("utf-8")
        global_id: str = base64.b64decode(bt).decode()  # format "typeName_id"

        data: List[str | ID] = global_id.split("_")
        return {
            "type_name": data[0],
            "instance_id": cast(ID, data[1])
        }

    @classmethod
    async def get_id_from_model_instance(cls, model_instance: Model) -> strawberry.ID:
        id_ins = cls.encode_id(cls.__name__, model_instance.pk)  # format "typeName_id"
        return id_ins

    @classmethod
    async def from_model_instance(cls: Type[A], model_instance: Model) -> A:
        # If model_instance is not correct raise error
        if not isinstance(model_instance, cls._model_):
            raise TypeError(f"Instance is not of type {cls._model_.__name__}")

        attrs = {}
        # Iterating over the fields of the type, in order to map to the model
        for name, val in cls.__annotations__.items():
            # If field is a function, skip
            if isinstance(val, StrawberryAnnotation):
                continue

            # If fild is the id, get and set encoded unique id
            if name.lower() == "id":
                attrs[name] = await cls.get_id_from_model_instance(model_instance)
                continue

            # Add field to dict of attrs
            attrs[name] = model_instance.__getattribute__(name)
        # Creating corresponding type attrs
        return cls(**attrs)


async def node_resolver(self, id: strawberry.ID) -> Optional[Node]:
    id_decoded: DecodedID = Node.decode_id(id)

    # Import is done here to avoid circular import
    from storefront_backend.api.schema import schema

    type_name = id_decoded.get("type_name")
    schema_type: TypeDefinition = cast(TypeDefinition, schema.get_type_by_name(type_name))
    node_class: Node = cast(Node, schema_type.origin)
    model = node_class._model_

    model_instance = await model.objects.aget(pk=id_decoded.get("instance_id"))

    return await node_class.from_model_instance(model_instance)
