import types
import inspect


F_FOUND = {}


def object_to_serializable(obj):
    global F_FOUND
    if obj is None:
        return "null"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if obj is float("Inf"):
        return "Infinity"
    if obj is float("-Inf"):
        return "-Infinity"
    if obj is float("NaN"):
        return "NaN"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, bytes):
        return '"' + str(list(bytearray(obj))) + '"'
    if isinstance(obj, str):
        return '"' + obj.replace("\\", "\\\\").replace('"', '\\"') + '"'
    if isinstance(obj, set):
        return set_to_dict(obj)
    if isinstance(obj, frozenset):
        return frozenset_to_dict(obj)
    if isinstance(obj, tuple):
        return tuple_to_dict(obj)
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        return obj
    if inspect.isfunction(obj):
        res = function_to_dict(obj)
        F_FOUND = {}
        return res
    if inspect.ismodule(obj):
        return module_to_dict(obj)
    if isinstance(obj, types.CodeType):
        return code_to_dict(obj)
    if isinstance(obj, types.CellType):
        return cell_to_dict(obj)

    raise TypeError()


def module_to_dict(obj):
    return {"module_type": obj.__name__}


def function_to_dict(obj):
    gls = gather_gls(obj, obj.__code__)

    return {
        "function_type": {
            "__globals__": gls,
            "__name__": obj.__name__,
            "__code__": code_to_dict(obj.__code__),
            "__defaults__": obj.__defaults__,
            "__closure__": obj.__closure__,
        }
    }


def gather_gls(obj, obj_code):
    global F_FOUND
    F_FOUND[obj] = True
    gls = {}
    for i in obj_code.co_names:
        try:
            if (
                inspect.isfunction(obj.__globals__[i])
                and obj.__globals__[i] not in F_FOUND
            ):
                gls[i] = function_to_dict(obj.__globals__[i])
            elif inspect.ismodule(obj.__globals__[i]):
                gls[i] = module_to_dict(obj.__globals__[i])
            elif isinstance(
                obj.__globals__[i],
                (set, dict, list, int, float, bool, type(None), tuple, str),
            ):
                gls[i] = obj.__globals__[i]
        except KeyError:
            pass
    for i in obj_code.co_consts:
        if isinstance(i, types.CodeType):
            gls.update(gather_gls(obj, i))
    return gls


def cell_to_dict(obj):
    return {"cell_type": obj.cell_contents}


def set_to_dict(obj):
    return {"set_type": list(obj)}


def frozenset_to_dict(obj):
    return {"frozenset_type": list(obj)}


def tuple_to_dict(obj):
    return {"tuple_type": list(obj)}


def code_to_dict(obj):
    return {
        "code_type": {
            "co_argcount": obj.co_argcount,
            "co_posonlyargcount": obj.co_posonlyargcount,
            "co_kwonlyargcount": obj.co_kwonlyargcount,
            "co_nlocals": obj.co_nlocals,
            "co_stacksize": obj.co_stacksize,
            "co_flags": obj.co_flags,
            "co_code": obj.co_code.decode("cp1251"),
            "co_consts": obj.co_consts,
            "co_names": obj.co_names,
            "co_varnames": obj.co_varnames,
            "co_filename": obj.co_filename,
            "co_name": obj.co_name,
            "co_firstlineno": obj.co_firstlineno,
            "co_lnotab": obj.co_lnotab.decode("cp1251"),
            "co_freevars": obj.co_freevars,
            "co_cellvars": obj.co_cellvars,
        }
    }


def dict_to_object(args):
    if "function_type" in args:
        return dict_to_func(args["function_type"])
    if "module_type" in args:
        return dict_to_module(args["module_type"])
    if "code_type" in args:
        return dict_to_code(args["code_type"])
    if "cell_type" in args:
        return dict_to_cell(args["cell_type"])
    if "tuple_type" in args:
        return tuple(args["tuple_type"])
    if "frozenset_type" in args:
        return frozenset(args["frozenset_type"])
    if "set_type" in args:
        return set(args["set_type"])

    return args


def dict_to_module(obj):
    try:
        return __import__(obj)
    except ModuleNotFoundError as module_not_found:
        raise ImportError(str(obj) + " not found") from module_not_found


def dict_to_cell(obj):
    return types.CellType(obj)


def dict_to_code(obj):
    print(obj["co_lnotab"])
    return types.CodeType(
        obj["co_argcount"],
        obj["co_posonlyargcount"],
        obj["co_kwonlyargcount"],
        obj["co_nlocals"],
        obj["co_stacksize"],
        obj["co_flags"],
        bytes(obj["co_code"], "cp1251"),
        obj["co_consts"],
        obj["co_names"],
        obj["co_varnames"],
        obj["co_filename"],
        obj["co_name"],
        obj["co_firstlineno"],
        bytes(obj["co_lnotab"], "cp1251"),
        obj["co_freevars"],
        obj["co_cellvars"],
    )


def collect_funcs(obj, is_visited):
    for i in obj.__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = attr
            is_visited = collect_funcs(attr, is_visited)
    return is_visited


def set_funcs(obj, is_visited, gls):
    for i in obj.__globals__:
        attr = obj.__globals__[i]
        if inspect.isfunction(attr) and attr.__name__ not in is_visited:
            is_visited[attr.__name__] = True
            attr.__globals__.update(gls)
            is_visited = set_funcs(attr, is_visited, gls)
    return is_visited


def dict_to_func(obj):
    closure = None
    if obj["__closure__"] is not None:
        closure = obj["__closure__"]
    res = types.FunctionType(
        globals=obj["__globals__"],
        code=obj["__code__"],
        name=obj["__name__"],
        closure=closure,
    )
    try:
        setattr(res, "__defaults__", obj["__defaults__"])
    except TypeError:
        pass
    funcs = collect_funcs(res, {})
    funcs.update({res.__name__: res})
    set_funcs(res, {res.__name__: True}, funcs)
    res.__globals__.update(funcs)
    res.__globals__["__builtins__"] = __import__("builtins")
    return res
