import importlib
from datetime import datetime


def get_datetime_dirname():
    now = str(datetime.now()).split('.')[0]
    now = '___'.join(now.split())
    now = '-'.join(now.split(':'))
    return now


def is_include(keywords, text: str):
    for k in keywords:
        if k.lower() in text.lower(): return True
    return False


def import_class(_class_path: str):
    *_module_path, _class_name = _class_path.split('.')
    _module = importlib.import_module('.'.join(_module_path))
    _class = getattr(_module, _class_name)
    return _class
