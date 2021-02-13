# Zokusei - Fast and simple Python declarative classes


Zokusei is Japanese for attribute.
Its APIs are modeled after attrs,
but it's using minimal metaprogramming instead of code generation
and it tries to avoid feature cost.


```pycon

>>> from zokusei import DataClass, attribute, as_dict

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

>>> as_dict(sc)
{'a_number': 1, 'list_of_numbers': [1, 2, 3]}

>>> SomeClass()
SomeClass(a_number=42, list_of_numbers=[])

```
