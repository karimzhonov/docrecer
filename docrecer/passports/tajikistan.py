from docrecer.core.base.base_passport import PassportData


class TajikistanPasport(PassportData):
    _is_it_keywords = ['Чумхурии', 'Точикистон', 'Tajikistan']
    _set_coordinate_key = 'Republic of Tajikistan'

    @staticmethod
    def get_citizenship():
        return 'Таджикистан'

    def parse_serial_number(self, text):
        for word in text.split(' '):
            if self._validate_number(word) is not None:
                self.number = self._validate_number(word)

    def extract_data(self, data):
        PassportData.extract_data(self, data)
        if self._word_height is None: return
        # Extrac bottom
        text = self._find_row_by_delta_height(19 * self._word_height, data, 10 * self._word_height)
        if not text: return
        text = text.replace(' ', '')
        text = [t for t in text.split('<') if t]
        if self.surname is None: self.surname = self._delete_chars(text[1][3:])
        if self.name is None: self.name = self._delete_chars(text[2])
        if self.number is None: self.parse_serial_number(text[3][:9])
        if self.gender is None:
            if 'm' in text[3][20].lower():
                self.gender = 'Мужской'
            elif 'f' in text[3][20].lower():
                self.gender = 'Женский'
        self._extrac_authority(data)
        # extrac authority
        text = self._find_row_by_delta_height(17 * self._word_height, data)
        if not text: return
        self.authority = self._delete_chars(text)
