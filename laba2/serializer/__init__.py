"""
Serialization tool, use dump, load, dumps and loads to serialize objects in supported languages

Use get_formats to get all markup formats
"""

from .utility import *
import custom_json
import custom_yaml
import custom_pickle


_formats = {}

modules = [custom_json, custom_pickle, custom_yaml]


def dumps(obj, format):
    """Converts object to string and returns it."""

    dumper = get_serializer(format)
    simple = utility.dump(obj)
    return dumper.dumps(simple)


def dump(obj, fp, format=""):
    """Converts object to string and write it to file."""

    dumper = get_serializer(format, fp.name)
    simple = utility.dump(obj)
    return dumper.dump(simple, fp)


def loads(s, format):
    """Converts string to object and returns it."""

    loader = get_serializer(format)
    simple = loader.loads(s)
    return utility.load(simple)


def load(fp, format=""):
    """Converts string from file to object and returns it."""

    loader = get_serializer(format, fp.name)
    simple = loader.load(fp)
    return utility.load(simple)


def convert_str(s, ilang, olang):
    """Converts serialized data from one markup language to another.
    Returns new string.
    """

    loader = get_serializer(ilang)
    dumper = get_serializer(olang)

    if loader is dumper:
        return s
    else:
        return dumper.dumps(loader.loads(s))


def convert_file(input, output, ilang="", olang=""):
    """Converts serialized data from one markup language to another.
    Creates new file.
    """

    loader = get_serializer(ilang, input)
    read_mod = loader.read_mod

    dumper = get_serializer(olang, output)
    write_mod = dumper.write_mod

    if loader is dumper:
        return

    with open(input, read_mod) as fp:
        loaded_data = loader.load(fp)

    with open(output, write_mod) as fp:
        dumper.dump(loaded_data, fp)


def get_formats():
    """Returns the list of supported markup formats."""

    return list(_formats)


def get_serializer(format="", filename=""):
    """Fabric method that returns serializer for specified format"""

    if format == "":
        format = filename.rpartition(".")[2]
    return create_serializer(format.lower())


def create_serializer(serialization_format):
    try:
        return _formats[serialization_format]
    except KeyError:
        raise ValueError(f"The lang '{serialization_format}' is not supported")


def _populate_formats(format_modules):
    for module in format_modules:
        for extention in set(map(str.lower, module.extentions)):
            if not _formats.setdefault(extention, module) is module:
                raise ValueError(
                    f"Same extention {extention} is used twice ({_formats[extention].__name__} and {module.__name__})"
                )


_populate_formats(modules)
