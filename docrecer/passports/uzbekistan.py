from docrecer.core.base.base_passport import PassportData


class UzbekistanInternationalPassport(PassportData):
    _is_it_keywords = ['Uzbekistan']
    _set_coordinate_key = 'PASSPORT'

    @staticmethod
    def get_citizenship():
        return 'Узбекистан'

    def parse_serial_number(self, text):
        for word in text.split(' '):
            if len(word) == 9:
                _number = self._validate_number(word[2:])
                if _number is not None:
                    self.number = _number
                    self.serial = word[:2]

    def extract_data(self, data):
        PassportData.extract_data(self, data)
        if self._word_height is None: return
        # Extrac data from bottom
        text = self._find_row_by_delta_height(20 * self._word_height, data, 10 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        text = text.replace(' ', '')
        text = [t for t in text.split('<') if t]
        if not self.name: self.name = self._delete_chars(text[2])
        if not self.surname: self.surname = self._delete_chars(text[1][3:])
        if not self.middle_name: self.middle_name = self._delete_chars(' '.join(text[3:5]))
        if self.serial is None or self.number is None: self.parse_serial_number(text[5][:9])
        if self.gender is None:
            if 'm' in text[5][20].lower():
                self.gender = 'Мужской'
            elif 'f' in text[5][20].lower():
                self.gender = 'Женский'
        # Extrac Authory
        text = self._find_row_by_delta_height(15 * self._word_height, data, 3 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        text = text.split(' ')
        for i, word in enumerate(text):
            try:
                int(word)
            except ValueError:
                self.authority = self._delete_chars(f'{word} {text[i + 1]}')
