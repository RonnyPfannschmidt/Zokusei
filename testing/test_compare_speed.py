from functools import partial
from typing import Callable

import pytest
from operator import eq
import attr
import dataclasses

from zokusei import field, DataClass

FIELDS_6 = ("one", "two", "three", "four", "five", "six")
FIELDS_2 = FIELDS_6[:2]





class Attrs:
    field = attr.field
    base = object
    decorate = attr.s

    @classmethod
    def decorator(cls, class_config):
        return partial(cls.decorate, **class_config)
    type_args = staticmethod(lambda x: {})

class PyDataclass:
    field = dataclasses.field
    base = object
    decorate = dataclasses.dataclass

    @classmethod
    def decorator(cls, class_config):
        return partial(cls.decorate, **class_config)

    type_args = staticmethod(lambda x: {})


class Zokusei:
    field = field
    base = DataClass
    decorator = staticmethod(lambda t: (lambda x: x))
    type_args = staticmethod(lambda t: t)



def simple(base: type, decorate, field: Callable[[], object], type_config: dict):
    @decorate
    class Example(base, **type_config):
        one: int = field()
        two: int = field()
    return Example,  FIELDS_2


def subclasses(base, decorate, field, type_config):

    @decorate
    class Example(base, **type_config):
        one: int = field()
        two: int = field()

    @decorate
    class Example2(Example):
        three: int = field()

    @decorate
    class Example3(Example2):
        four: int = field()


    @decorate
    class Example4(Example3):
        five: int = field()


    @decorate
    class Example5(Example4):
        six: int = field()

    return Example5, FIELDS_6




@pytest.fixture(params=[simple, subclasses])
def class_template(request):
    return request.param

class Classmaker(DataClass):
    backend_spec = field()
    class_template = field()
    class_config = field()

    def __call__(self):
        return self.class_template(
            base=self.backend_spec.base,
            decorate=self.backend_spec.decorator(self.class_config),
            field=self.backend_spec.field,
            type_config=self.backend_spec.type_args(self.class_config),
        )



@pytest.fixture(params=[Attrs, PyDataclass, Zokusei])
def classmaker(request, class_template):
    m = request.node.get_closest_marker("class_config", pytest.mark.class_config)
    return Classmaker(backend_spec = request.param, class_template=class_template, class_config=m.kwargs)


def test_make_class(benchmark, classmaker):
    benchmark(classmaker)

@pytest.fixture
def _made_class(classmaker):
    return classmaker()

@pytest.fixture
def klass(_made_class):
    return _made_class[0]


@pytest.fixture
def args(_made_class):
    return _made_class[1]

def test_make_instance(benchmark, klass, args):
    benchmark(klass, **dict.fromkeys(args, 1))


def test_repr(benchmark, klass, args):

    inst = klass(**dict.fromkeys(args, 1))

    benchmark(repr, inst)


@pytest.mark.class_config(eq=True)
def test_eq(benchmark, klass,  args):
    inst = klass(**dict.fromkeys(args, 1))
    inst2 = klass(**dict.fromkeys(args, 1))
    assert inst == inst2
    benchmark(eq, inst, inst2)