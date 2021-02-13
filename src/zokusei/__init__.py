from functools import total_ordering as _total_ordering
from operator import attrgetter as _attrgetter
from typing import Any
from typing import NamedTuple
from typing import Optional


_INTENAL_STORE = "_zokusei_attributes"


class DataClass:
    __slots__ = ()

    def __init_subclass__(cls, *addons, eq=None, order=None, **args):
        if _INTENAL_STORE not in cls.__dict__:
            setattr(cls, _INTENAL_STORE, _pluck_attributes(cls))
        if "__init__" not in cls.__dict__:
            cls.__init__ = _make_init(cls)
        if "__repr__" not in cls.__dict__:
            cls.__repr__ = _default_repr
        if eq and "__eq__" not in cls.__dict__:
            cls.__eq__ = _make_eq(cls)

        if order is not None and "__lt__" not in cls.__dict__:
            cls.__lt__ = _make_lt(cls)
            _total_ordering(cls)


def _make_init(current_klass):

    attributes = getattr(current_klass, _INTENAL_STORE)

    # todo: positional args
    def __init__(self, **kw):
        # todo: cooperation
        for name, attribute in attributes.items():
            try:
                val = kw.pop(name)
            except KeyError:
                val = attribute.default
            setattr(self, name, val)
        super(current_klass, self).__init__(**kw)

    return __init__


def _make_eq(current_klass):
    attributes = getattr(current_klass, _INTENAL_STORE)
    getter = _attrgetter(*attributes)

    def __eq__(self, other, _getter=getter):
        # todo: cooperation
        return _getter(self) == _getter(other)
        # and super(current_klass, self).__eq__(other)

    return __eq__


def _make_lt(current_klass):
    attributes = getattr(current_klass, _INTENAL_STORE)
    getter = _attrgetter(*(name for name, attr in attributes.items() if attr.order))

    def __lt__(self, other, _getter=getter):
        return _getter(self) < _getter(other)

    __lt__.__qualname__ = f"{current_klass.__qualname__}.__lt__"
    return __lt__


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


def _default_repr(self):
    params = ", ".join(
        f"{attribute.name}={getattr(self, attribute.name)!r}"
        for attribute in attributes(type(self))
    )

    return f"{type(self).__name__}({params})"


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


def attribute(*k, **kw):
    return Attribute(*k, **kw)


def as_dict(obj):
    return {attr.name: getattr(obj, attr.name) for attr in attributes(type(obj))}
