from .tajikistan import TajikistanPasport
from .uzbekistan import UzbekistanInternationalPassport
from .russia import RussianPassport
from ..core.base.base_passport import PassportData


class BasePassport(PassportData):
    @classmethod
    def is_it(cls, data):
        return True
