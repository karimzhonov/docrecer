from dataclasses import dataclass
from docrecer.core.data import Data
from docrecer.core.base.base_patent import PatentData
from docrecer.core.base.base_passport import PassportData
from docrecer.core.base.base_migration_card import MigrationCardData
from docrecer.core.base.base_snils import SnilsData


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

