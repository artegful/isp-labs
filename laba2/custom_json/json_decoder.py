"""Json decoder that converts json format to objects"""

class JsonDecoder:
    def load(self, obj):
        (item, obj) = self.__json_to_obj(obj)
        obj = obj.lstrip()
        if obj != "":
            raise ValueError("bad format")
        else:
            return item


    def __json_to_obj(self, obj):
        obj = obj.lstrip()

        if obj.startswith("{"):
            return self.__json_to_dict(obj)
        if obj.startswith("["):
            return self.__json_to_list(obj)
        if obj.startswith('"'):
            return self.__json_to_string(obj)
        if obj.startswith(self.int_const):
            return self.__json_to_numeric(obj)
        if obj.startswith("false"):
            return self.__json_to_custom("false", False)(obj)
        if obj.startswith("true"):
            return self.__json_to_custom("true", True)(obj)
        if obj.startswith("null"):
            return self.__json_to_custom("null", None)(obj)

        raise ValueError("can't decode")


    def __json_to_dict(self, objs):
        res = {}
        objs = remove_prefix(objs, "{").lstrip()
        while not objs.startswith("}"):
            (key, objs) = self.__json_to_obj(objs)
            objs = remove_prefix(objs, ":")
            (value, objs) = self.__json_to_obj(objs)
            res[key] = value
            objs = remove_prefix(objs, ",").lstrip()
        return res, remove_prefix(objs, "}")


    def __json_to_list(self, objs):
        res = []
        objs = remove_prefix(objs, "[").lstrip()
        while not objs.startswith("]"):
            (value, objs) = self.__json_to_obj(objs)
            res.append(value)
            objs = remove_prefix(objs, ",").lstrip()
        return res, remove_prefix(objs, "]")


    def __json_to_numeric(self, obj):
        for i in range(len(obj)):
            if obj[i] not in self.int_const and obj[i] != ".":
                try:
                    return int(obj[:i]), obj[i:]
                except ValueError:
                    return float(obj[:i]), obj[i:]

        try:
            return int(obj), ""
        except ValueError:
            return float(obj), ""


    def __json_to_string(self, obj):
        obj = remove_prefix(obj, '"')
        tmp = obj.find('"')
        return obj[:tmp], obj[tmp + 1 :]


    int_const = tuple("1 2 3 4 5 6 7 8 9 0 -".split(" "))


    def __json_to_custom(self, word, value=None):
        def result(obj):
            if obj.startswith(word):
                return value, obj[len(word) :]

        result.__name__ = "parse_%s" % word
        return result


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text
