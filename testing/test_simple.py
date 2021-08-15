import pytest

from zokusei import as_dict
from zokusei import attributes
from zokusei import DataClass
from zokusei import field


class Example(DataClass):
    name: str = field()
    age: int = field()


class Point(DataClass, eq=True):  # type: ignore
    x: int = field()
    y: int = field()


class Priorized(DataClass, order=True):  # type: ignore
    priority: int = field(order=True)
    name: str = field(order=False)


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


def test_order():
    first = Priorized(priority=1, name="win")
    tied = Priorized(priority=1, name="win2")
    different = Priorized(priority=2, name="nay")

    assert not first < tied
    assert not tied < first
    assert first > tied
    assert tied > first
    assert not first == tied  # sorting the same but is not the same

    assert different > first
    assert first < different

    assert (
        sorted(
            [
                different,
                first,
                tied,
            ]
        )
        == [first, tied, different]
    )

    assert sorted([tied, first]) == [tied, first]
