from typing import Optional

__package__ = "zokusei"

from ._general_methods import _add_methods, attributes


class DataClass:
    __slots__ = ()

    @classmethod
    def __init_subclass__(cls, *, eq: bool = False, order: bool = False):

        _add_methods(cls, eq, order)


class Attribute:

    # name: Optional[str]
    # default: Optional[object]
    # order: Optional[bool]

    def __set_name__(self, owner, name):
        self.name = name

    def __init__(
        self,
        name: Optional[str] = None,
        default: Optional[object] = None,
        order: Optional[bool] = None,
    ):
        self.name = name
        self.default = default
        self.order = order


def field(*k, **kw):
    return Attribute(*k, **kw)


def as_dict(obj):
    return {attr.name: getattr(obj, attr.name) for attr in attributes(type(obj))}
