"""Module used for loading objects from serializable form created by dumper module"""

import builtins
import inspect
import types
from importlib import import_module


_loaded = {}

_moduleattrs = ("__name__", "__doc__")

_loaded_funcattrs = (
    "__code__",
    "__globals__",
    "__name__",
    "__defaults__",
    "__closure__",
)

_funcattrs = (
    "__qualname__",
    "__doc__",
    "__dict__",
    "__module__",
    "__kwdefaults__",
    "__annotations__",
)

_codeattrs = (
    "co_argcount",
    "co_posonlyargcount",
    "co_kwonlyargcount",
    "co_nlocals",
    "co_stacksize",
    "co_flags",
    "co_code",
    "co_consts",
    "co_names",
    "co_varnames",
    "co_filename",
    "co_name",
    "co_firstlineno",
    "co_lnotab",
    "co_freevars",
    "co_cellvars",
)


_builtin = {
    **{
        str(getattr(builtins, key)): getattr(builtins, key)
        for key in dir(builtins)
        if isinstance(getattr(builtins, key), type)
    },
    **{
        str(getattr(types, key)): getattr(types, key)
        for key in dir(types)
        if isinstance(getattr(types, key), type)
    },
    str(type(Ellipsis)): type(Ellipsis),
    str(type(NotImplemented)): type(NotImplemented),
}


def load(serialized_object):
    """Create object from serializable form"""
    _loaded.clear()
    _create_empty_objects(serialized_object)
    return _load_object(serialized_object)


def _create_empty_objects(serialized_object):
    if isinstance(serialized_object, list):
        return tuple(_create_empty_objects(element) for element in serialized_object)

    if not isinstance(serialized_object, dict):
        return serialized_object

    loaded_data = _try_load_data_from_id(serialized_object["__id__"])[0]

    if not isinstance(loaded_data, int):
        return loaded_data

    address = loaded_data

    loaded_class_object = _create_empty_objects(serialized_object["__class__"])
    if "__bases__" in serialized_object:
        loaded_object = _create_with_cls(loaded_class_object, serialized_object)
    else:
        loaded_object = _create_buildin(loaded_class_object, serialized_object)

    _loaded[address] = (loaded_object, False)

    for value in serialized_object.values():
        _create_empty_objects(value)
    return loaded_object


def _load_object(serialized_object):
    if isinstance(serialized_object, list):
        return tuple(_load_object(element) for element in serialized_object)

    if not isinstance(serialized_object, dict):
        return serialized_object

    empty_object, is_ready = _try_load_data_from_id(serialized_object["__id__"])
    if is_ready:
        return empty_object

    _load_object(serialized_object["__class__"])

    if "__bases__" in serialized_object:
        return _load_class(empty_object, serialized_object)

    loaded_object = _populate_empty_object(
        type(empty_object), empty_object, serialized_object
    )
    if loaded_object is None:
        loaded_object = empty_object
    _loaded[_load_id(serialized_object["__id__"])] = (loaded_object, True)

    if "__dict__" in serialized_object:
        setattr(loaded_object, "__dict__", _load_object(serialized_object["__dict__"]))

    if "__slots__" in serialized_object:
        for key, value in _load_object(serialized_object["__slots__"]).items():
            setattr(loaded_object, key, value)

    return loaded_object


def _load_id(id_str):
    return int(id_str.rpartition(" at ")[2], 0)


def _try_load_data_from_id(data_id):
    if data_id.startswith("<"):
        return (_builtin[data_id], True)

    id_int = _load_id(data_id)
    return _loaded.get(id_int, (id_int, False))


def _create_buildin(cls, dct):
    if cls in (bool, int, float, complex, str):
        return cls(dct["__value__"])
    if cls in (bytes, bytearray):
        return cls.fromhex(dct["__value__"])
    if cls is range:
        return cls(*dct["__value__"])
    if cls is type(None):
        return None
    if cls is type(Ellipsis):
        return Ellipsis
    if cls is type(NotImplemented):
        return NotImplemented
    if cls is object:
        return object()
    if cls is memoryview:
        return cls(bytes())
    if cls is types.MappingProxyType:
        return cls({})
    if cls is types.MethodType:
        return cls(
            _create_empty_objects(dct["__func__"]),
            _create_empty_objects(dct["__self__"]),
        )
    if cls is types.FunctionType:
        return _load_id
    if cls is types.CodeType:
        return cls(*(_create_empty_objects(dct[key]) for key in _codeattrs))
    if cls is types.ModuleType:
        return cls(*(_create_empty_objects(dct[key]) for key in _moduleattrs))

    return cls()


def _create_with_cls(cls, obj):
    return cls(
        obj["__name__"],
        _create_empty_objects(obj["__bases__"]),
        {"__slots__": obj["__slots__"]} if "__slots__" in obj else {},
    )


def _populate_empty_object(cls, obj, dct):
    if cls is list:
        return obj.extend(_load_object(obj) for obj in dct["__value__"])
    if cls is tuple:
        return tuple(_load_object(obj) for obj in dct["__value__"])
    if cls is memoryview:
        return memoryview(_load_object(dct["__value__"]))
    if cls is set:
        return obj.update(_load_object(obj) for obj in dct["__value__"])
    if cls is frozenset:
        return frozenset(_load_object(obj) for obj in dct["__value__"])
    if cls is dict:
        return _load_dict(obj, dct)
    if cls is types.MappingProxyType:
        return _load_mapping(dct)
    if cls is types.MethodType:
        return types.MethodType(
            _load_object(dct["__func__"]),
            _load_object(dct["__self__"]),
        )
    if cls is types.FunctionType:
        return _load_func(dct)
    if cls is types.CellType:
        return types.CellType(_load_object(dct["__value__"]))
    if cls is types.ModuleType:
        return import_module(dct["__name__"])

    return None


def _load_dict(obj, dct):
    for pair in dct["__value__"]:
        obj[_load_object(pair[0])] = _load_object(pair[1])


def _load_mapping(dct):
    tmp = {}
    _load_dict(tmp, dct)
    return types.MappingProxyType(tmp)


def _load_globals():
    from .. import __name__ as border

    for frame in inspect.stack():
        if not frame[1].startswith(border):
            return frame[0].f_globals


def _load_func(dct):
    gls = _load_globals()
    tmp = {key: _load_object(dct[key]) for key in _loaded_funcattrs}
    gls.update(tmp["__globals__"])
    tmp["__globals__"] = gls

    func = types.FunctionType(*tmp.values())
    for key in _funcattrs:
        setattr(func, key, _load_object(dct[key]))

    return func


def _load_class(cls, loading_dict):
    _loaded[_load_id(loading_dict["__id__"])] = (cls, True)
    _load_object(loading_dict["__class__"])
    _load_object(loading_dict["__bases__"])

    for key, value in _load_object(loading_dict["__dict__"]).items():
        setattr(cls, key, value)

    return cls
