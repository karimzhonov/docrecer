import json
from pathlib import Path
from types import NoneType


class Serializer:
    def to_json(self, enable_none = True):
        return serializer(self.__dict__, enable_none)

    def save_as_json(self, path, enable_none = True):
        Path(path).write_text(json.dumps(self.to_json(enable_none), indent=4, ensure_ascii=False), errors='ignore')


def serializer(obj, enable_none = True):
    if not enable_none:
        if isinstance(obj, NoneType):
            return '-'
    if isinstance(obj, Serializer):
        return obj.to_json()
    elif isinstance(obj, (list, tuple, set)):
        return list_serializer(obj)
    elif isinstance(obj, dict):
        return dict_serializer(obj)
    elif isinstance(obj, float):
        return str(obj)
    else:
        return obj


def dict_serializer(d: dict):
    return {key: serializer(value) for key, value in d.items() if (not key.startswith('_')) and value}


def list_serializer(l):
    return [serializer(value) for value in l]
