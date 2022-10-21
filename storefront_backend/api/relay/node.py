from __future__ import annotations

import base64
from typing import ClassVar, Union, Optional, TypedDict

import strawberry
from django.db.models import Model
from strawberry.annotation import StrawberryAnnotation


class DecodedID(TypedDict):
    type_name: str
    instance_id: str


@strawberry.interface
class Node:
    id: strawberry.ID
    _model_: ClassVar[Model]

    @classmethod
    def encode_id(cls, type_name: str, node_id: str):
        id_ins = f"{type_name}_{node_id}".encode("utf-8")  # format "typeName_id"
        calc_id: Union[strawberry.ID, str] = base64.b64encode(id_ins).decode()
        return calc_id

    @classmethod
    def get_id_from_model_instance(cls, model_instance: Model) -> strawberry.ID:
        id_ins = cls.encode_id(cls.__name__, model_instance.pk)  # format "typeName_id"
        return id_ins

    @classmethod
    def decode_id(cls, id: strawberry.ID) -> DecodedID:
        bt = id.encode("utf-8")
        global_id = base64.b64decode(bt).decode()  # format "typeName_id"

        data = global_id.split("_")
        return {
            "type_name": data[0],
            "instance_id": data[1]
        }

    @classmethod
    def from_model_instance(cls, model_instance: Model) -> Node:
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
                attrs[name] = cls.get_id_from_model_instance(model_instance)
                continue

            # Add field to dict of attrs
            attrs[name] = model_instance.__getattribute__(name)
        # Creating corresponding type attrs
        return cls(**attrs)


async def node_resolver(self, id: strawberry.ID) -> Optional[Node]:
    id_decoded = Node.decode_id(id)

    # Import is done here to avoid circular import
    from storefront_backend.api.schema import schema

    node_class: Node = schema.get_type_by_name(id_decoded.get("type_name")).origin
    model = node_class._model_

    model_instance = await model.objects.aget(pk=id_decoded.get("instance_id"))

    return node_class.from_model_instance(model_instance)
