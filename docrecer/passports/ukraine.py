import re
from docrecer.core.base.base_passport import PassportData


class UkrainePassport(PassportData):
    _is_it_keywords = ['ukraine']
    _set_coordinate_key = 'passport'

    def get_citizenship(self, data):
        return "Украина"

    def parse_serial_number(self, text):
        if len(text) == 8:
            self.serial = self._delete_chars(text[:2])
            self.number = self._validate_number(text[2:])

    def _extrac_with_coordinate(self, data):
        text = self._find_row_same_word('P<UKR', data, 5 * self._word_height, include_word=True)
        if text:
            text = [t for t in text.replace(' ', '').split('<') if t]
            if not self.name: self.name = self._delete_chars(text[2])
            if not self.surname: self.surname = self._delete_chars(text[1][3:])
            if not self.serial or not self.number: self.parse_serial_number(text[3])
            if not self.gender:
                if 'm' in text[4].lower():
                    self.gender = 'Male'
                elif 'f' in text[4].lower():
                    self.gender = 'Female'
    def _extrac_with_regexp(self, data):
        # Extrac all date
        text = self._find_row_same_word(self._set_coordinate_key,data, 50 * self._word_height, 5 * self._word_height / 7)
        date = re.findall(r'\d\d\s\D\D\D\D\D\D\D\s\d\d', text)
        _date = []
        for d in date:
            d = d.split(' ')
            d[1] = d[1].split('/')[1].capitalize()
            d = '-'.join(d)
            _date.append(d)
        if not self.birth_date: self.birth_date = _date[0]
        if not self.issue_date: self.issue_date = _date[1]
        if not self.expiration_date: self.expiration_date = _date[2]
        # Extrac authority
        if not self.authority:
            for word in re.findall(r'[0-9]+', text):
                if len(word) == 4:
                    self.authority = word


    def extract_data(self, data, config, image):
        PassportData.extract_data(self, data, config, image)
        self._extrac_with_coordinate(data)
        self._extrac_with_regexp(data)