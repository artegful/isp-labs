import pytest
import types
import serializer

type_to_attrs = {
    types.CodeType: serializer.utility.dumper._codeattrs,
    types.FunctionType: serializer.utility.dumper._funcattrs,
}


def assert_restored_object(obj):
    for language in serializer.get_formats():
        serialized = serializer.dumps(obj, language)
        restored = serializer.loads(serialized, language)

        attrs = type_to_attrs[type(obj)]

        for attr in attrs:
            if attr in ("__closure__", "__module__"):
                continue

            assert getattr(obj, attr) == getattr(restored, attr)


def foo():
    pass


def f_globals():
    return math.sin(x)


def indent(x):
    def closure(y):
        return x + y

    return closure


def test_foo_code():
    subject = foo.__code__

    assert_restored_object(subject)


def test_foo_func():
    subject = foo

    assert_restored_object(subject)


def test_globals_func():
    subject = f_globals
    import math

    globals()["math"] = math
    globals()["x"] = 5
    result = subject()

    del math

    serialized = serializer.dumps(subject, "json")

    del globals()["math"]
    del globals()["x"]

    restored = serializer.loads(serialized, "json")

    restored_result = restored()

    assert_restored_object(subject)
    assert result == restored_result


def test_closure_func():
    subject = indent(5)
    result = subject(10)
    serialized = serializer.dumps(subject, "json")
    restored = serializer.loads(serialized, "json")

    restored_result = restored(10)

    assert_restored_object(subject)
    assert result == restored_result


def test_indent_func():
    subject = indent
    x_result = subject(5)
    y_result = x_result(10)

    serialized = serializer.dumps(subject, "json")
    restored = serializer.loads(serialized, "json")

    restored_x_result = restored(5)
    restored_y_result = restored_x_result(10)

    assert_restored_object(subject)
    assert_restored_object(x_result)

    assert y_result == restored_y_result


def test_lambda():
    subject = lambda x: x * 10
    assert_restored_object(subject)
