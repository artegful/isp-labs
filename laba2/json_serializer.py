import serializer


def dumps(obj):
    return _dumps(obj).replace("\n", "")


def dump(obj, file_name):
    string = _dumps(obj)
    try:
        with open(file_name, "w") as file:
            file.write(string)
    except FileNotFoundError as file_not_found:
        raise FileNotFoundError("file doesn't exist") from file_not_found


def loads(string):
    idx = 0
    try:
        while string[idx] == " " or string[idx] == "\n":
            idx += 1
    except IndexError:
        pass
    obj, idx = parse_symbol(string, idx)

    try:
        while True:
            if string[idx] != " " and string[idx] != "\n":
                raise StopIteration(idx)
            idx += 1
    except IndexError:
        pass
    return obj


def load(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.read()
    except FileNotFoundError as file_not_found:
        raise FileNotFoundError("file doesn't exist") from file_not_found
    return loads(data)


def dumps_list(obj, step="", new_step=""):
    if not obj:
        return "[]"

    new_step = "\n" + new_step
    res = "[" + new_step

    for i in range(len(obj) - 1):
        res += (
            step
            + _dumps(obj[i], step, new_step.replace("\n", "") + step)
            + ","
            + new_step
        )
    res += (
        step + _dumps(obj[-1], step, new_step.replace("\n", "") + step) + new_step + "]"
    )
    return res


def dumps_dict(obj, step="", new_step=""):
    if not obj:
        return "{}"

    new_step = "\n" + new_step
    res = "{" + new_step
    keys = list(obj)
    for i in keys[:-1]:
        res += (
            step
            + '"'
            + str(i)
            + '"'
            + ": "
            + _dumps(obj[i], step, new_step.replace("\n", "") + step)
            + ","
            + new_step
        )
    res += (
        step
        + '"'
        + str(keys[-1])
        + '"'
        + ": "
        + _dumps(obj[keys[-1]], step, new_step.replace("\n", "") + step)
        + new_step
        + "}"
    )

    return res


def _dumps(obj, step=" ", new_step=""):
    serializable_object = serializer.object_to_serializable(obj)

    if isinstance(serializable_object, str):
        return serializable_object
    if isinstance(serializable_object, dict):
        return dumps_dict(serializable_object, step, new_step)
    if isinstance(serializable_object, list):
        return dumps_list(serializable_object, step, new_step)

    raise TypeError()


def parse_symbol(string, idx):
    if string[idx] == '"':
        obj, idx = parse_string(string, idx + 1)
    elif string[idx].isdigit() or (string[idx] == "-" and string[idx + 1].isdigit()):
        obj, idx = parse_digit(string, idx)
    elif string[idx] == "{":
        obj, idx = parse_dict(string, idx + 1)
    elif string[idx] == "[":
        obj, idx = parse_list(string, idx + 1)
    elif string[idx] == "n" and string[idx : idx + 4] == "null":
        obj = None
        idx += 4
    elif string[idx] == "t" and string[idx : idx + 4] == "true":
        obj = True
        idx += 4
    elif string[idx] == "f" and string[idx : idx + 5] == "false":
        obj = False
        idx += 5
    elif string[idx] == "N" and string[idx : idx + 3] == "NaN":
        obj = False
        idx += 3
    elif string[idx] == "I" and string[idx : idx + 8] == "Infinity":
        obj = float("Infinity")
        idx += 8
    elif string[idx] == "-" and string[idx : idx + 9] == "-Infinity":
        obj = float("-Infinity")
        idx += 9
    else:
        raise StopIteration(idx)
    return obj, idx


def parse_dict(string, idx):
    args = {}
    comma = False
    colon = False
    phase = False
    temp = None

    try:
        next_char = string[idx]
    except IndexError as index_error:
        raise StopIteration(idx) from index_error
    while True:
        if next_char == "}":
            break

        if next_char in (" ", "\\n"):
            idx += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(idx)
            idx += 1
            phase = False
            comma = False
        elif next_char == ":":
            if colon is False:
                raise StopIteration(idx)
            idx += 1
            phase = True
            colon = False
        elif not comma and not phase:
            if next_char == '"':
                obj, idx = parse_string(string, idx + 1)
                if obj in args:
                    raise StopIteration(idx)
                temp = obj
                phase = False
                colon = True
            else:
                raise StopIteration(idx)
        elif not colon and phase:
            obj, idx = parse_symbol(string, idx)
            args[temp] = obj

            comma = True
        else:
            raise StopIteration(idx)
        try:
            next_char = string[idx]
        except IndexError as index_error:
            raise StopIteration(idx) from index_error

    if not comma and not colon and len(args) != 0:
        raise StopIteration(idx)

    return serializer.dict_to_object(args), idx + 1


def parse_string(string, idx):
    first = idx
    opened = False
    try:
        while string[idx] != '"' or opened:
            if string[idx] == "\\":
                opened = not opened
            else:
                opened = False
            idx += 1
    except IndexError as index_error:
        raise StopIteration(idx) from index_error
    return string[first:idx], idx + 1


def parse_digit(string, idx):
    first = idx
    try:
        while (
            string[idx] == "."
            or string[idx].isdigit()
            or string[idx] == "e"
            or string[idx] == "E"
            or string[idx] == "-"
            or string[idx] == "+"
        ):
            idx += 1
    except IndexError:
        pass
    res = string[first:idx]
    try:
        return int(res), idx
    except ValueError:
        try:
            return float(res), idx
        except ValueError:
            raise StopIteration(idx)


def parse_list(string, idx):
    args = []
    comma = False

    try:
        next_char = string[idx]
    except IndexError:
        raise StopIteration(idx)
    while True:
        if next_char == "]":
            break

        if next_char in (" ", "\\n"):
            idx += 1
        elif next_char == ",":
            if comma is False:
                raise StopIteration(idx)
            idx += 1
            comma = False
        elif not comma:
            obj, idx = parse_symbol(string, idx)
            args.append(obj)

            comma = True
        else:
            raise StopIteration(idx)
        try:
            next_char = string[idx]
        except IndexError as index_error:
            raise StopIteration(idx) from index_error
    if not comma and len(args) != 0:
        raise StopIteration(idx)
    return list(args), idx + 1
