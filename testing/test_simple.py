import pytest

from zokusei import as_dict
from zokusei import attribute
from zokusei import attributes
from zokusei import DataClass


class Example(DataClass):
    name: str = attribute()
    age: int = attribute()

class Point(DataClass, eq=True):
    x: int = attribute()
    y: int = attribute()


@pytest.fixture
def santa():
    return Example(name="santa", age=42)


def test_attributes():
    print(attributes(Example))


def test_repr(santa):
    assert repr(santa) == "Example(name='santa', age=42)"


def test_as_dict(santa):
    assert as_dict(santa) == {"name": santa.name, "age": santa.age}


def test_eq():
    a = Point(x=1, y=1)
    b = Point(x=1, y=1)
    assert a == b

    c = Point(x=1, y=3)

    assert a != c