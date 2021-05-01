from io import FileIO
from typing import Any, IO
import json
import serializer

class JsonSerializer:
    base_dumps = json.dumps
    base_dump = json.dump
    base_loads = json.loads
    base_load = json.load

    def dump(self, obj, file):
        if file:
            serializable_object = serializer.get_serializable_object(obj)
            JsonSerializer.base_dump(serializable_object, file, indent=4)
        else:
            raise ValueError("File transfer aborted")

    def dumps(self, obj):
        serializable_object = serializer.get_serializable_object(obj)
        return JsonSerializer.base_dumps(serializable_object)

    def load(self, name, file, globals):
        if file:
            raw_object = JsonSerializer.base_load(file)
            return serializer.create_object(raw_object, name, globals)
        else:
            raise ValueError("File transfer aborted")

    def loads(self, name, line, globals):
        raw_object = JsonSerializer.base_loads(line)
        return serializer.create_object(raw_object, name, globals)