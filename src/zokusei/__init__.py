from functools import total_ordering as _total_ordering
from typing import Any
from typing import NamedTuple
from typing import Optional

from zokusei._general_methods import _make_init, _make_eq, _default_repr, _make_lt

_INTENAL_STORE = "_zokusei_attributes"


class DataClass:
    __slots__ = ()

    def __init_subclass__(cls, *addons, eq=None, order=None, **args):
        if _INTENAL_STORE not in cls.__dict__:
            setattr(cls, _INTENAL_STORE, _pluck_attributes(cls))
        attributes = cls.__dict__[]
        if "__init__" not in cls.__dict__:
            cls.__init__ = _make_init(cls)
        if "__repr__" not in cls.__dict__:
            cls.__repr__ = _default_repr
        if eq and "__eq__" not in cls.__dict__:
            cls.__eq__ = _make_eq(cls)

        if order is not None and "__lt__" not in cls.__dict__:
            cls.__lt__ = _make_lt(cls)
            _total_ordering(cls)


class SimpleAttribute:
    pass


class DefaultSimpleAttribute(NamedTuple):
    default: Optional[Any] = None


def attributes(cls):
    return [
        Attribute(name=name, default=attribute.default)
        if isinstance(attribute, (SimpleAttribute, DefaultSimpleAttribute))
        else attribute
        for mro_element in reversed(cls.__mro__)
        for name, attribute in getattr(mro_element, _INTENAL_STORE, {}).items()
    ]


def _pluck_attributes(cls):
    plucked = {k: v for k, v in cls.__dict__.items() if isinstance(v, Attribute)}
    for k in plucked:
        delattr(cls, k)
    return plucked


class Attribute(DataClass):
    _zokusei_attributes = {
        "name": DefaultSimpleAttribute(None),
        "default": DefaultSimpleAttribute(None),
        "order": DefaultSimpleAttribute(None),
    }

    def __set_name__(self, owner, name):
        self.name = name


def field(*k, **kw):
    return Attribute(*k, **kw)


def as_dict(obj):
    return {attr.name: getattr(obj, attr.name) for attr in attributes(type(obj))}
