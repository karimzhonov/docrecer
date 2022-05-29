from dataclasses import dataclass
from docrecer.core.data import Data, is_other_document
from docrecer.core.ocrs.response import PageData
from docrecer.utils import is_include
from docrecer.conf import SUPPORT_MIGRATION_CARDS


@dataclass
class MigrationCardData(Data):
    _support_classes = SUPPORT_MIGRATION_CARDS

    serial: str = None
    number: str = None

    def _extrac_serial(self, data: PageData):
        pass

    def _extrac_number(self, data: PageData):
        pass

    @staticmethod
    def is_migration_card_data(data: PageData) -> bool:
        from docrecer.core.base import is_snils
        return is_migration_card(data) and not (
                is_snils(data) or
                is_other_document(data)
        )


def is_migration_card(data: PageData):
    keywords = ('departure', 'migrat')
    return is_include(keywords, data.text)
