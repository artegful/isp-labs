import pytest
import serializer


class SimpleCls:
    pass


class ContainerCls:
    none = None
    bool = True
    int = 1251
    float = 22 / 7
    str = "string"
    tuple = tuple("tuple")
    list = list("list")
    dict = {"d": "i", "c": "t"}


class SlotsCls:
    __slots__ = ("a", "b", "c")


class MetaCls(type):
    pass


class ParentCls(metaclass=MetaCls):
    pass


class ChildCls(ParentCls, ContainerCls, metaclass=MetaCls):
    pass


def assert_vars(obj):
    for language in serializer.get_formats():
        serialized = serializer.dumps(obj, language)
        restored = serializer.loads(serialized, language)

        for var in vars(obj):
            if var not in ("__dict__", "__weakref__", "__module__"):
                assert getattr(obj, var) == getattr(restored, var)


def assert_slots(obj):
    for language in serializer.get_formats():
        serialized = serializer.dumps(obj, language)
        restored = serializer.loads(serialized, language)

        for var in type(obj).__slots__:
            if hasattr(obj, var) and hasattr(restored, var):
                assert getattr(obj, var) == getattr(restored, var)
            else:
                assert hasattr(obj, var) == hasattr(restored, var)


def test_simple_cls():
    subject = SimpleCls

    assert_vars(subject)


def test_container_cls():
    subject = ContainerCls

    assert_vars(subject)


def test_container_obj():
    subject = ContainerCls()

    assert_vars(type(subject))
    assert_vars(subject)


def test_slots():
    subject = SlotsCls()

    assert_slots(subject)


def test_inheritance():
    subject = ChildCls

    assert_vars(subject)

    serialized = serializer.dumps(subject, "json")
    restored = serializer.loads(serialized, "json")

    assert restored.__bases__[0].__name__ == subject.__bases__[0].__name__
    assert restored.__bases__[1].__name__ == subject.__bases__[1].__name__
    assert type(restored).__name__ == type(subject).__name__
