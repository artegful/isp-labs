import json

extentions = ["json"]
read_mod = "r"
write_mod = "w"


def dumps(obj):
    return json.dumps(obj, indent=4)


def dump(obj, fp):
    fp.write(dumps(obj))


def loads(s):
    return json.loads(s)


def load(fp):
    return loads(fp.read())
