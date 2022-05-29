from dataclasses import dataclass
from docrecer.core.data import Data, is_other_document
from docrecer.core.ocrs.response import PageData
from docrecer.utils import is_include
from docrecer.conf import SUPPORT_PASSPORTS


@dataclass
class PassportData(Data):
    _support_classes = SUPPORT_PASSPORTS

    serial: str = None
    number: str = None
    birth_date: str = None
    citizenship: str = None
    issue_date: str = None
    expiration_date: str = None
    gender: str = None
    surname: str = None
    name: str = None
    middle_name: str = None
    birth_place: str = None
    authority: str = None

    @staticmethod
    def get_citizenship():
        pass

    def parse_serial_number(self, text):
        pass

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

    def _extrac_gender(self, data: PageData):
        pass

    def _extrac_birth_place(self, data: PageData):
        pass

    def _exctrac_issue(self, data: PageData):
        pass

    def _extrac_exprition_date(self, data: PageData):
        pass

    def _extrac_authority(self, data: PageData):
        pass

    @staticmethod
    def is_passport_data(data: PageData) -> bool:
        from docrecer.core.base import is_patent, is_snils, is_migration_card

        return is_passport(data) and not (
                is_patent(data) or
                is_migration_card(data) or
                is_snils(data) or is_other_document(data)
        )


def is_passport(data: PageData):
    keywords = ('passpor', 'paspor', 'Шиноснома')
    return is_include(keywords, data.text)
