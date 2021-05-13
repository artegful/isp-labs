import yaml

extentions = ["yaml", "yml"]
read_mod = "r"
write_mod = "w"


def dumps(obj):
    return yaml.dump(obj)


def dump(obj, fp):
    fp.write(dumps(obj))


def loads(s):
    return yaml.safe_load(s)


def load(fp):
    return loads(fp.read())
