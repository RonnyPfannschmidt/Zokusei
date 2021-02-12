from typing import Any
from typing import NamedTuple
from typing import Optional

_INTENAL_STORE = "_zokusei_attributes"


class DataClass:
    __slots__ = ()

    def __init_subclass__(cls, *addons, eq=None,  **args):
        if _INTENAL_STORE not in cls.__dict__:
            setattr(cls, _INTENAL_STORE, _pluck_attributes(cls))
        if "__init__" not in cls.__dict__:
            cls.__init__ = _make_init(cls)
        if "__repr__" not in cls.__dict__:
            cls.__repr__ = _default_repr
        if eq and "__eq__" not in cls.__dict__:
            cls.__eq__ = _make_eq(cls)
        super()


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

    # todo: positional args
    def __eq__(self, other):
        print((name, getattr(self, name), getattr(other, name)) for name in attributes)
        # todo: cooperation
        return all(getattr(self, name) == getattr(other, name) for name in attributes) 
        # and super(current_klass, self).__eq__(other)

    return __eq__

def _default_ne(self, other):
    return not self == other

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
    }

    def __set_name__(self, owner, name):
        self.name = name


def attribute():
    return Attribute()


def as_dict(obj):
    return {attr.name: getattr(obj, attr.name) for attr in attributes(type(obj))}
