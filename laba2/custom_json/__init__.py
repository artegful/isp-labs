from .json_encoder import JsonEncoder
from .json_decoder import JsonDecoder

extentions = ["json"]
read_mod = "r"
write_mod = "w"


def dumps(obj):
    return JsonEncoder().dump(obj)


def dump(obj, fp):
    fp.write(dumps(obj))


def loads(obj):
    return JsonDecoder().load(obj)


def load(fp):
    return loads(fp.read())
