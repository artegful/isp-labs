import types
import json
import inspect


def get_serializable_object(py_object):

    if isinstance(py_object, types.FunctionType):
        return serialize_function(py_object)
    elif isinstance(py_object, types.ModuleType):
        return serialize_module(py_object)
    else:
        raise ValueError("Can't serialize this object")


def serialize_function(py_object):

    payload = { py_object.__name__: {
    "__type__": "function",
    "__name__": f"{py_object.__name__}",
    "__qualname__": f"{py_object.__qualname__}",
    "__annotations__": f"{py_object.__annotations__}",
    "__kwdefaults__": f"{py_object.__kwdefaults__}",
    "__defaults__": f"{py_object.__defaults__}",
    "__module__": f"{py_object.__module__}",
    "__doc__": f"{py_object.__doc__}",
    "__closure__": f"{py_object.__closure__}",
    "__globals__": f"{py_object.__globals__}",
    "__code__": {
    "co_argcount": f"{py_object.__code__.co_argcount}",
    "co_kwonlyargcount": f"{py_object.__code__.co_kwonlyargcount}",
    "co_posonlyargcount": f"{py_object.__code__.co_posonlyargcount}",
    "co_nlocals": f"{py_object.__code__.co_nlocals}",
    "co_stacksize": f"{py_object.__code__.co_stacksize}",
    "co_flags": f"{py_object.__code__.co_flags}",
    "co_code": py_object.__code__.co_code.decode("cp1251"),
    "co_consts": f"{py_object.__code__.co_consts}",
    "co_names": f"{py_object.__code__.co_names}",
    "co_varnames": f"{py_object.__code__.co_varnames}",
    "co_filename": f"<stdin>",
    "co_name": f"{py_object.__code__.co_name}",
    "co_firstlineno": f"{py_object.__code__.co_firstlineno}",
    "co_lnotab": py_object.__code__.co_lnotab.decode("cp1251"),
    "co_freevars": f"{py_object.__code__.co_freevars}",
    "co_cellvars": f"{py_object.__code__.co_cellvars}"
    }
    }
    }

    for used_object in py_object.__code__.co_names:
        if used_object in py_object.__globals__:
            payload.update(get_used_object(used_object, py_object.__globals__))
    return payload


def get_used_object(used_object_name, globals):
    if (isinstance(globals[used_object_name], (int, float, str, bool))):
        return serialize_primitive(used_object_name, globals[used_object_name])
    else:
        return get_serializable_object(globals[used_object_name])


def serialize_primitive(name, value):
    return {name: {
        "__type__": "primitive",
        "__name__": name,
        "__value__": value
    }}


def serialize_module(py_object):
    return { py_object.__name__: {
        "__type__": "module",
        "__name__": py_object.__name__
    }
    }


def create_object(serializable_dict, name, globals):
    serializable_object = serializable_dict[name]

    if (serializable_object["__type__"] == "primitive"):
        return create_primitive(serializable_object)
    elif (serializable_object["__type__"] == "function"):
        return create_function(serializable_object, serializable_dict, globals)
    elif (serializable_object["__type__"] == "module"):
        return create_module(serializable_object, globals)


def create_primitive(serializable_object):
    return serializable_object["__value__"]


def create_function(serializable_object, serializable_dict, globals):
    serialized_code = serializable_object["__code__"]

    code = types.CodeType(int(serialized_code["co_argcount"]), int(serialized_code["co_kwonlyargcount"]), int(serialized_code["co_posonlyargcount"]), 
    int(serialized_code["co_nlocals"]), int(serialized_code["co_stacksize"]), int(serialized_code["co_flags"]),
    bytes(serialized_code["co_code"], "cp1251"), eval(serialized_code["co_consts"]), eval(serialized_code["co_names"]), eval(serialized_code["co_varnames"]),
    serialized_code["co_filename"], serialized_code["co_name"], int(serialized_code["co_firstlineno"]), bytes(serialized_code["co_lnotab"], "cp1251"))

    dependencies = {}

    for name in serializable_dict:
        if (name in code.co_names and name not in globals):
            dependencies[name] = create_object(serializable_dict, name, globals)

    dependencies.update(globals)

    return types.FunctionType(code, dependencies)


def create_module(py_object, globals):
    return __import__(py_object["__name__"])

