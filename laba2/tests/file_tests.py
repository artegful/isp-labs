import pytest
import os
import serializer


class ContainerCls:
    none = None
    bool = True
    int = 1251
    float = 22 / 7
    str = "string"
    tuple = tuple("tuple")
    list = list("list")
    dict = {"d": "i", "c": "t"}


def assert_vars(obj):
    for language in serializer.get_formats():

        loader = serializer.get_serializer(language)
        read_mode = loader.read_mod
        write_mode = loader.write_mod

        name = f"test.{language}"

        with open(name, write_mode) as fp:
            serializer.dump(obj, fp, language)

        with open(name, read_mode) as fp:
            try:
                restored = serializer.load(fp)
            finally:
                os.remove(name)

        for var in vars(obj):
            if var not in ("__dict__", "__weakref__", "__module__"):
                assert getattr(obj, var) == getattr(restored, var)


def test_container_cls():
    subject = ContainerCls

    assert_vars(subject)


def test_container_obj():
    subject = ContainerCls()

    assert_vars(subject)
    