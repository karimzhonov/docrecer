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
        return ''

    def parse_serial_number(self, text):
        self.number = self._delete_chars(text)

    @staticmethod
    def _search_from_entities(data, key: str):
        for value in data.entities:
            if value['name'] == key and not value['text'] == '-':
                return value['text']
        return ''

    def _extrac_serial_number(self, data):
        self.parse_serial_number(self._search_from_entities(data, 'number'))

    def _extrac_surname(self, data):
        self.surname = self._delete_chars(self._search_from_entities(data, 'surname'))

    def _extrac_name(self, data):
        self.name = self._delete_chars(self._search_from_entities(data, 'name'))

    def _extrac_middle_name(self, data):
        self.middle_name = self._delete_chars(self._search_from_entities(data, 'middle_name'))

    def _extrac_birth_date(self, data):
        self.birth_date = self._validate_date(self._search_from_entities(data, 'birth_date'))

    def _extrac_gender(self, data):
        self.gender = self._delete_chars(self._search_from_entities(data, 'gender'))

    def _extrac_birth_place(self, data):
        self.birth_place = self._delete_chars(self._search_from_entities(data, 'birth_place'))

    def _exctrac_issue(self, data):
        self.issue_date = self._validate_date(self._search_from_entities(data, 'issue_date'))

    def _extrac_exprition_date(self, data):
        self.expiration_date = self._validate_date(self._search_from_entities(data, 'expiration_date'))

    def _extrac_authority(self, data: PageData):
        self.authority = self._delete_chars(self._search_from_entities(data, 'issued_by'))

    @staticmethod
    def is_passport_data(data: PageData) -> bool:
        from docrecer.core.base import is_patent, is_snils, is_migration_card

        return is_passport(data) and not (
                is_patent(data) or
                is_migration_card(data) or
                is_snils(data) or is_other_document(data)
        )

    def extract_data(self, data):
        self.citizenship = self.get_citizenship()
        self._extrac_serial_number(data)
        self._extrac_surname(data)
        self._extrac_name(data)
        self._extrac_middle_name(data)
        self._extrac_gender(data)
        self._extrac_birth_date(data)
        self._extrac_birth_place(data)
        self._exctrac_issue(data)
        self._extrac_exprition_date(data)
        self._extrac_authority(data)
        # Extra extrac
        self._set_coordinate(data)


def is_passport(data: PageData):
    keywords = ('passpor', 'paspor', 'Шиноснома', 'Паспорт')
    return is_include(keywords, data.text)
