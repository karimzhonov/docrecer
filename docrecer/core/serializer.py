import json
from pathlib import Path


class Serializer:
    def to_json(self):
        return serializer(self.__dict__)

    def save_as_json(self, path):
        Path(path).write_text(json.dumps(self.to_json(), indent=4, ensure_ascii=False), errors='ignore')


def serializer(obj):
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
    return {key: serializer(value) for key, value in d.items() if not key.startswith('_')}


def list_serializer(l):
    return [serializer(value) for value in l]
