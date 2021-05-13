import unittest
import test
import json_serializer


def converter(obj):
    return json_serializer.loads(json_serializer.dumps(obj))


class TestSerializer(unittest.TestCase):

    def __init__(self, methodName):
        super().__init__(methodName)

    def test_empty_object(self):
        objects = test.objects
        self.assertEqual(objects, converter(objects))

    def test_simple_string(self):
        objects = test.string
        self.assertEqual(objects, converter(objects))

    def test_simple_obj_1(self):
        objects = test.t1
        self.assertEqual(objects, converter(objects))

    def test_simple_obj_2(self):
        objects = test.t2
        self.assertEqual(objects, converter(objects))

    def test_simple_obj_3(self):
        objects = test.t3
        self.assertEqual(objects, converter(objects))

    def test_simple_func(self):
        objects = test.simple_func
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(), converter(objects)())

    def test_recursion_func(self):
        objects = test.simple_recursion
        self.assertEqual(objects.__code__, converter(objects.__code__))
        try:
            converter(objects)()
        except RecursionError:
            pass

    def test_cycle_recursion_func(self):
        objects = test.double_func_recursion_2
        self.assertEqual(objects.__code__, converter(objects.__code__))
        try:
            converter(objects)()
        except RecursionError:
            pass

    def test_func_with_globals_and_builtins(self):
        objects = test.func_with_globals_and_builtins
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(), converter(objects)())

    def test_func_in_func(self):
        objects = test.func_in_func
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(2, 3, 4), converter(objects)(2, 3, 4))

    def test_func_with_defaults(self):
        objects = test.func_with_defaults
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(), converter(objects)())

    def test_tuple_returner(self):
        objects = test.tuple_returner
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(2, 3, 4, 5), converter(objects)(2, 3, 4, 5))

    def test_set_returner(self):
        objects = test.set_returner
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(2, 3, 4, 5), converter(objects)(2, 3, 4, 5))

    def test_func_with_args_sum(self):
        objects = test.func_with_args_sum
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(2, 3, 4, 5), converter(objects)(2, 3, 4, 5))

    def test_func_with_args_d(self):
        objects = test.func_with_args_d
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(a=4,b=3), converter(objects)(a=4,b=3))

    def test_decorator(self):

        def test_func():
            return 'hh'

        objects = test.counter
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(test_func)(), converter(objects)(test_func)())

    def test_check_decorator(self):
        objects = test.check_decorator
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(), converter(objects)())

    def test_simplified_defaults(self):
        objects = test.p
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects()(), converter(objects)()())

    def test_simple_lambda(self):
        objects = test.simplelambda
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(3), converter(objects)(3))

    def test_lambda_in_lambda(self):
        objects = test.lambda_in_lambda
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(3), converter(objects)(3))

    def test_lambda_in_function(self):
        objects = test.lambda_in_function
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(3), converter(objects)(3))

    def test_some_decorators(self):
        objects = test.some_decorators
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(3), converter(objects)(3))


    def test_using_module(self):
        objects = test.using_module
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(3), converter(objects)(3))


    def test_using_logging(self):
        objects = test.using_logging_module
        self.assertEqual(objects.__code__, converter(objects.__code__))
        self.assertEqual(objects(), converter(objects)())
