import math
import logging

t1 = [[[[[[[[[[[3, [[[[[[[[[[[[[[[[[[[[[[[[[[[55.3, [[[[[[[[[[4]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]

t2 = {(3, 4), 5}

t3 = ({(4)}, 6)

objects = [{}, set(), tuple(), []]

string = "4 43    43"


def simple_func():
    pass


def simple_recursion():
    return simple_recursion()


def double_func_recursion_1():
    return double_func_recursion_2()


def double_func_recursion_2():
    return double_func_recursion_1()


gl1 = 53


def func_with_globals_and_builtins():
    print(simple_func)
    return gl1


def func_in_func(a, f, l):
    print(a)

    def first(b):
        print(a + b)

        def second(c):
            print(a + b + c)

        second(l)

    first(f)


def func_with_defaults(a=1, b=3):
    return a + b


def tuple_returner(a, b, c, d):
    x = a + b
    y = c + d
    return (x, y)


def set_returner(a, b, c, d):
    x = a + b
    y = c + d
    return {x, y}


def func_with_args_sum(*args):
    return sum(args)


def func_with_args_d(**args):
    return args


def counter(func):
    count = 0

    def wrapper(*args):
        func(*args)
        nonlocal count
        count += 1
        print(count)

    return wrapper


@counter
def check_decorator():
    pass


def p(a=simple_func):
    return a


simplelambda = lambda x: x * x

lambda_in_lambda = lambda x: simplelambda(x) * x


def lambda_in_function(a=2):
    print(lambda_in_lambda(a))


@counter
@counter
@counter
def some_decorators(a=3):
    print("hello world")


def using_module(x):
    return math.sin(x)


def using_logging_module():
    logging.info("I am using logging")