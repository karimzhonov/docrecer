from dataclasses import dataclass
from .data import Data
from .base.base_patent import PatentData
from .base.base_passport import PassportData
from .base.base_migration_card import MigrationCardData
from .base.base_snils import SnilsData


@dataclass
class PersonalData(Data):

    passport: PassportData = PassportData()
    patent: PatentData = PatentData()
    migration_card: MigrationCardData = MigrationCardData()
    snils: SnilsData = SnilsData()

    def reset(self):
        self.snils.reset()
        self.passport.reset()
        self.patent.reset()
        self.migration_card.reset()

