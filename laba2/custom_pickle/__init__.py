import pickle

extentions = ["pickle"]
read_mod = "rb"
write_mod = "wb"


def dumps(obj):
    return pickle.dumps(obj)


def dump(obj, fp):
    fp.write(dumps(obj))


def loads(s):
    return pickle.loads(s)


def load(fp):
    return loads(fp.read())
