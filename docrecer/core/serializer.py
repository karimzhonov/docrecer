import json


class Serializer:

    def to_json(self):
        return serializer(self.__dict__)

    def save_as_json(self, path):
        with open(path, 'w') as file:
            json.dump(self.to_json(), file, indent=4, ensure_ascii=False)


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
