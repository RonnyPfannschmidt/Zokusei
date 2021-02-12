# Zokusei - Fast and simple python declarative classes


Zokusei is japanese for attribute.
its apis is modeled after attrs,
but its using minimal metaprogrammign instead of code generation
and it tries to avoid feature cost.


```pycon

>>> from zokusei import DataClass, attribute

>>> class SomeClass(DataClass):
...     a_number: int = attribute(default=42)
...     list_of_numbers: list[int] = attribute(factory=list)
...
...     def hard_math(self, another_number):
...         return self.a_number + sum(self.list_of_numbers) * another_number


>>> sc = SomeClass(1, [1, 2, 3])
>>> sc
SomeClass(a_number=1, list_of_numbers=[1, 2, 3])

>>> sc.hard_math(3)
19
>>> sc == SomeClass(1, [1, 2, 3])
True
>>> sc != SomeClass(2, [3, 2, 1])
True

>>> attr.asdict(sc)
{'a_number': 1, 'list_of_numbers': [1, 2, 3]}

>>> SomeClass()
SomeClass(a_number=42, list_of_numbers=[])

>>> C = attr.make_class("C", ["a", "b"])
>>> C("foo", "bar")
C(a='foo', b='bar')
from zokusei import DataClass, attribute

class User(zokusei.DataClass):
    id: int = attribute(repr=False)
    name: str = attribute()
    age: int = attribute(repr=False, eq=True)

```
