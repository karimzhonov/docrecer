from dataclasses import dataclass
from docrecer.core.data import Data, is_other_document
from docrecer.core.ocrs.response import PageData
from docrecer.utils import is_include
from docrecer.conf import SUPPORT_PATENTS


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
