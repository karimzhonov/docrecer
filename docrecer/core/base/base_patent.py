import importlib
from dataclasses import dataclass
from ..data import Data, is_other_document
from ..ocrs.response import PageData
from ...utils import is_include
from ...conf import SUPPORT_PATENTS, SUPPORT_PASSPORTS


@dataclass
class PatentData(Data):
    _support_classes = SUPPORT_PATENTS

    birth_date: str = None
    citizenship: str = None
    serial: str = None
    number: str = None
    surname: str = None
    name: str = None
    middle_name: str = None
    tin: str = None
    position: str = None
    issue_date: str = None
    authority: str = None
    passport_number: str = None
    passport_serial: str = None

    def _extrac_serial_number(self, data: PageData):
        pass

    def _extrac_surname(self, data: PageData):
        pass

    def _extrac_name(self, data: PageData):
        pass

    def _extrac_middle_name(self, data: PageData):
        pass

    def _extrac_birth_date(self, data: PageData):
        pass

    def _extrac_citizenship(self, data: PageData):
        pass

    def _extrac_position(self, data: PageData):
        pass

    def _extrac_tin(self, data: PageData):
        pass

    def _extrac_authority(self, data: PageData):
        pass

    def _extrac_issue_date(self, data: PageData):
        pass

    def parse_serial_number_passport(self, data, text):
        for _class_path in SUPPORT_PASSPORTS:
            *_module_path, _class_name = _class_path.split('.')
            _module = importlib.import_module('.'.join(_module_path))
            _class = getattr(_module, _class_name)
            if _class().get_citizenship(data) == self.citizenship:
                instance = _class()
                instance.parse_serial_number(text)
                self.passport_serial = instance.serial
                self.passport_number = instance.number

    @staticmethod
    def is_patent_data(data: PageData) -> bool:
        from docrecer.core.base import is_migration_card, is_snils
        return is_patent(data) and not (
                is_migration_card(data) or
                is_snils(data) or
                is_other_document(data)
        )


def is_patent(data: PageData):
    keywords = ('патент',)
    return is_include(keywords, data.text)
