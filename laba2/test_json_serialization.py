import pytest
import logging

from JsonSerializer import JsonSerializer


global_x = 5


def sum_function(a, b):
    return a + b


def calling_function():
    return "I am calling " + called_function()


def called_function():
    return "and I was called"


def function_using_module():
    logging.info("42")

    return "just used module"


def function_using_global():
    return global_x


serializer = JsonSerializer()


def test_serialize_sum_function():
    with open("sum_function.txt", "w") as file:
        serializer.dump(sum_function, file)


def test_serialize_calling_function():
    with open("calling_function.txt", "w") as file:
        serializer.dump(calling_function, file)


def test_serialize_function_using_module():
    with open("function_using_module.txt", "w") as file:
        serializer.dump(function_using_module, file)


def test_serialize_function_using_global():
    with open("function_using_global.txt", "w") as file:
        serializer.dump(function_using_global, file)