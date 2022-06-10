from dataclasses import dataclass
from ..data import Data, is_other_document
from ..ocrs.response import PageData
from ...utils import is_include
from ...conf import SUPPORT_SNILSS


@dataclass
class SnilsData(Data):
    _support_classes = SUPPORT_SNILSS

    number: str = None

    def _extrac_number(self, data: PageData):
        pass

    @staticmethod
    def is_snils_data(data: PageData) -> bool:
        return is_snils(data) and not (
            is_other_document(data)
        )


def is_snils(data: PageData):
    keywords = ('страховое', 'пенсионного')
    return is_include(keywords, data.text)
