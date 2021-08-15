from functools import total_ordering as _total_ordering
from operator import attrgetter as _attrgetter


_INTERNAL_STORE = "_zokusei_attributes"


def _make_init(current_klass, attributes):

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


def _pluck_attributes(cls):
    from zokusei import Attribute

    plucked = {k: v for k, v in cls.__dict__.items() if v.__class__ is Attribute}
    for k in plucked:
        delattr(cls, k)
    return plucked


def _make_eq(current_klass, attributes):
    getter = _attrgetter(*attributes)

    def __eq__(self, other, _getter=getter) -> bool:
        # todo: cooperation
        return _getter(self) == _getter(other)
        # and super(current_klass, self).__eq__(other)

    return __eq__


def _default_repr(self) -> str:
    params = ", ".join(
        f"{attribute.name}={getattr(self, attribute.name)!r}"
        for attribute in attributes(type(self))
    )

    return f"{type(self).__name__}({params})"


def _make_lt(current_klass, attributes):

    getter = _attrgetter(*(name for name, attr in attributes.items() if attr.order))

    def __lt__(self, other, _getter=getter):
        return _getter(self) < _getter(other)

    __lt__.__qualname__ = f"{current_klass.__qualname__}.__lt__"
    return __lt__


def _add_methods(cls, eq, order):
    attributes = cls.__dict__.get(_INTERNAL_STORE)
    if attributes is None:
        attributes = _pluck_attributes(cls)
        setattr(cls, _INTERNAL_STORE, attributes)

    if "__init__" not in cls.__dict__:
        cls.__init__ = _make_init(cls, attributes)
    if "__repr__" not in cls.__dict__:
        cls.__repr__ = _default_repr
    if eq and "__eq__" not in cls.__dict__:
        cls.__eq__ = _make_eq(cls, attributes)

    if order and "__lt__" not in cls.__dict__:
        cls.__lt__ = _make_lt(cls, attributes)
        _total_ordering(cls)


def attributes(cls):
    return [
        attribute
        for mro_element in reversed(cls.__mro__)
        for name, attribute in getattr(mro_element, _INTERNAL_STORE, {}).items()
    ]
