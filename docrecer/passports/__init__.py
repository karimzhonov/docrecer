from docrecer.core.base.base_passport import PassportData
from .tajikistan import TajikistanPasport
from .uzbekistan import UzbekistanInternationalPassport
from .russia import RussianPassport
from .ukraine import UkrainePassport
from .kyrgyz import KyrgyzPassport


class BasePassport(PassportData):
    @classmethod
    def is_it(cls, data):
        return True
