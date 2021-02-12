from zokusei import DataClass, attribute, attributes, as_dict

class Example(DataClass):
    name: str = attribute()
    age: int  = attribute()


def test_repr():
    print(attributes(Example))

    santa = Example(name="santa", age=42)
    assert repr(santa) == "Example(name='santa', age=42)"

    assert as_dict(santa) == {"name": santa.name, "age": santa.age}



