from .yamlparser import YamlParser

extentions = ["yaml", "yml"]
read_mod = "r"
write_mod = "w"


def dumps(obj):
    return YamlParser().dumps(obj)


def dump(obj, fp):
    fp.write(dumps(obj))


def loads(obj):
    return YamlParser().loads(obj)


def load(fp):
    return loads(fp.read())
