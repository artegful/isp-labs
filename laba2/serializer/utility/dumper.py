"""Module used for dumping objects into serializable form"""

import builtins
import types
import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


_dumped = []

_moduleattrs = ("__name__", "__doc__")

_funcattrs = (
    "__name__",
    "__qualname__",
    "__doc__",
    "__dict__",
    "__module__",
    "__closure__",
    "__defaults__",
    "__kwdefaults__",
    "__annotations__",
    "__code__",
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

_builtin = (
    *(
        getattr(builtins, key)
        for key in dir(builtins)
        if isinstance(getattr(builtins, key), type)
    ),
    *(
        getattr(types, key)
        for key in dir(types)
        if isinstance(getattr(types, key), type)
    ),
    type(Ellipsis),
    type(NotImplemented),
)


def dump(obj):
    """Convert object to serializable format"""
    _dumped.clear()
    return _dump(obj)


def _dump(obj):
    def _dump_type(cls):
        if id(cls) in _dumped:
            return {"__id__": _get_extended_id(cls)}

        nonlocal obj, obj_dict
        if cls in _builtin:
            if obj_dict is not None:
                _dump_builtin(cls, obj, obj_dict)
            return {"__id__": str(cls)}

        return _dump_custom_class(cls)

    def _dump_custom_class(cls):
        _dumped.append(id(cls))
        dumping_dict = {"__id__": _get_id(cls)}
        dumping_dict["__class__"] = _dump(type(cls))
        dumping_dict["__name__"] = getattr(cls, "__name__")

        bases_list = []
        for base in getattr(cls, "__bases__"):
            bases_list.append(_dump_type(base))
        dumping_dict["__bases__"] = bases_list

        cls_dict = getattr(cls, "__dict__")
        dumping_dict["__dict__"] = _dump(cls_dict)

        if obj_dict is not None:
            if "__slots__" in cls_dict:
                slots = {}
                for attr in cls_dict["__slots__"]:
                    if hasattr(obj, attr):
                        slots[attr] = getattr(obj, attr)
                obj_dict.setdefault("__slots__", {}).update(slots)
            elif "__dict__" not in obj_dict:
                if hasattr(obj, "__dict__"):
                    obj_dict["__dict__"] = _dump(getattr(obj, "__dict__"))

        return dumping_dict

    if isinstance(obj, tuple):
        return _dump_as_list(obj)
    if type(obj) in (type(None), bool, int, float, str):
        return obj

    if isinstance(obj, type):
        obj_dict = None
        return _dump_type(obj)

    if id(obj) in _dumped:
        return {"__id__": _get_extended_id(obj)}

    _dumped.append(id(obj))
    obj_dict = {"__id__": _get_id(obj), "__class__": None}
    obj_dict["__class__"] = _dump_type(type(obj))
    if "__slots__" in obj_dict:
        obj_dict["__slots__"] = _dump(obj_dict["__slots__"])
    return obj_dict


def _dump_builtin(cls, obj, obj_dict):
    if cls in (type(None), type(Ellipsis), type(NotImplemented), object):
        return

    if cls in (bool, int, float, complex):
        _dump_value(str(obj), obj_dict)
    elif cls in (list, set, frozenset):
        _dump_value(tuple(obj), obj_dict)
    elif cls in (dict, types.MappingProxyType):
        obj_dict.update({"__value__": _dump_mapping(obj)})
    elif cls is str:
        _dump_value(obj, obj_dict)
    elif cls is tuple:
        _dump_value(obj, obj_dict)
    elif cls is range:
        _dump_value((obj.start, obj.stop, obj.step), obj_dict)
    elif cls is bytes:
        _dump_value(bytes.hex(obj, " ", 1), obj_dict)
    elif cls is bytearray:
        _dump_value(bytearray.hex(obj, " ", 1), obj_dict)
    elif cls is memoryview:
        _dump_value(obj.obj, obj_dict)
    elif cls is types.MethodType:
        obj_dict.update(
            {"__func__": _dump(obj.__func__), "__self__": _dump(obj.__self__)}
        )
    elif cls is types.FunctionType:
        _dump_attrs(_funcattrs, obj, obj_dict)
        _dump_globals(obj, obj_dict)
    elif cls is types.CodeType:
        _dump_attrs(_codeattrs, obj, obj_dict)
    elif cls is types.CellType:
        _dump_value(obj.cell_contents, obj_dict)
    elif cls is types.ModuleType:
        _dump_attrs(_moduleattrs, obj, obj_dict)
    else:
        raise TypeError(f"<{_get_extended_id(obj)}> has unsupported type")


def _dump_mapping(dct):
    tmp = []
    for key in dct:
        try:
            tmp.append([_dump(key), _dump(dct[key])])
        except TypeError as error:
            logging.warning(
                "Key <%s> in <%s> was skipped because of %s",
                str(key),
                _get_extended_id(dct),
                error,
            )
    return tmp


def _get_id(obj):
    return hex(id(obj))


def _get_extended_id(obj):
    if hasattr(obj, "__name__"):
        line = "'" + obj.__name__ + "'"
    else:
        line = "instance"
    line += " of '" + type(obj).__name__
    line += "' at " + _get_id(obj)
    return line


def _dump_value(obj, obj_dict):
    obj_dict.update({"__value__": _dump(obj)})


def _dump_attrs(attrs, obj, obj_dict):
    obj_dict.update({attr: _dump(getattr(obj, attr)) for attr in attrs})


def _dump_globals(func, obj_dict):
    def dump_globals(code):
        gls.extend(code.co_names)
        for const in code.co_consts:
            if isinstance(const, types.CodeType):
                dump_globals(const)

    gls = []
    dump_globals(func.__code__)
    g_dct = {var: func.__globals__[var] for var in func.__globals__ if var in gls}
    obj_dict["__globals__"] = _dump(g_dct)


def _dump_as_list(collection):
    tmp = []
    for obj in collection:
        try:
            tmp.append(_dump(obj))
        except TypeError as error:
            logging.warning(
                "<%s> was skipped because of %s", _get_extended_id(obj), error
            )
    return tmp
