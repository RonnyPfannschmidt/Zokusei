from operator import attrgetter as _attrgetter

from zokusei import _INTENAL_STORE, attributes


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


def _default_repr(self):
    params = ", ".join(
        f"{attribute.name}={getattr(self, attribute.name)!r}"
        for attribute in attributes(type(self))
    )

    return f"{type(self).__name__}({params})"


def _make_lt(current_klass):
    attributes = getattr(current_klass, _INTENAL_STORE)

    getter = _attrgetter(*(name for name, attr in attributes.items() if attr.order))

    def __lt__(self, other, _getter=getter):
        return _getter(self) < _getter(other)

    __lt__.__qualname__ = f"{current_klass.__qualname__}.__lt__"
    return __lt__