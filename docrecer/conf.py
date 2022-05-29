from enum import Enum


# OCRs
class OCRS(Enum):
    YANDEX = 'yandex'
    TESSERACT = 'tesseract'


SUPPORT_PASSPORTS = [
    'docrecer.passports.TajikistanPasport',
    'docrecer.passports.UzbekistanInternationalPassport',
]

SUPPORT_PATENTS = [
    'docrecer.patents.CardPatent',
]

SUPPORT_MIGRATION_CARDS = [
    'docrecer.migration_cards.PaperMigrationCard',
]

SUPPORT_SNILSS = [
    'docrecer.snilss.CardSnils',
]
