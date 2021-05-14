from yaml import safe_load, dump


class YamlParser:
    def dumps(self, obj):
        return dump(obj, indent=4)

    def loads(self, obj):
        return safe_load(obj)
