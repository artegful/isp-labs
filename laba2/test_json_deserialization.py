import pytest

from JsonSerializer import JsonSerializer

serializer = JsonSerializer()

def test_deserialize_sum_function():
    with open("sum_function.txt", "r") as file:
        func = serializer.load("sum_function", file, globals())

    assert func(10, 5) == 15


def test_deserialize_calling_function():
    with open("calling_function.txt", "r") as file:
        func = serializer.load("calling_function", file, globals())

    assert func() == "I am calling and I was called"


def test_deserialize_function_using_module():
    with open("function_using_module.txt", "r") as file:
        func = serializer.load("function_using_module", file, globals())

    assert func() == "just used module"


def test_deserialize_function_using_global():
    with open("function_using_global.txt", "r") as file:
        func = serializer.load("function_using_global", file, globals())

    assert func() == 5