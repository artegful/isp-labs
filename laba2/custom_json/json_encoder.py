"""Json encoder that converts objects to json""" 

class JsonEncoder:
    def __init__(self, tab="\t", crlf="\n"):
        self.__nesting_level = 0
        self.__tab = tab
        self.__crlf = crlf
        self.__joiner = "," + self.__crlf


    def dump(self, obj):
        if type(obj) in self.__json_type:
            return self.__json_type[type(obj)](self, obj)
        else:
            raise ValueError("can't encode: ", type(obj))


    def __add_indent(self, level=-1):
        if level != -1:
            self.__nesting_level = level
        return self.__nesting_level * self.__tab


    def __dict_to_json(self, objs):
        bracket = self.__json_brackets[type(objs)]
        if not objs:
            return bracket[0] + bracket[1]
        self.__nesting_level += 1
        return (
            bracket[0]
            + self.__crlf
            + self.__joiner.join(
                [
                    str(
                        self.__add_indent()
                        + self.dump(key)
                        + ": "
                        + self.dump(value)
                    )
                    for key, value in objs.items()
                ]
            )
            + self.__crlf
            + self.__add_indent(self.__nesting_level - 1)
            + bracket[1]
        )


    def __array_to_json(self, objs):
        bracket = self.__json_brackets[type(objs)]
        if not objs:
            return bracket[0] + bracket[1]
        self.__nesting_level += 1
        return (
            bracket[0]
            + self.__crlf
            + self.__joiner.join(
                [str(self.__add_indent() + self.dump(obj)) for obj in objs]
            )
            + self.__crlf
            + self.__add_indent(self.__nesting_level - 1)
            + bracket[1]
        )


    def __primitive_to_json(self, obj):
        return str(obj)


    def __bool_to_json(self, obj):
        return str(obj).lower()


    def __none_to_json(self, obj):
        return "null"


    def __string_to_json(self, obj):
        bracket = self.__json_brackets[type(obj)]
        return bracket[0] + str(obj) + bracket[1]


    __json_brackets = {
        dict: ("{", "}"),
        list: ("[", "]"),
        tuple: ("[", "]"),
        str: ('"', '"'),
    }


    __json_type = {
        int: __primitive_to_json,
        float: __primitive_to_json,
        str: __string_to_json,
        bool: __bool_to_json,
        dict: __dict_to_json,
        list: __array_to_json,
        tuple: __array_to_json,
        type(None): __none_to_json,
    }
