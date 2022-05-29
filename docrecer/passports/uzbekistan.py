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

    def _extrac_serial_number(self, data):
        text = self._find_row_same_word('PASSPORT', data, 3 * self._word_height)
        if not text: return
        self.parse_serial_number(text)

    def _extrac_surname(self, data):
        text = self._find_row_by_delta_height(2.5 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        self.surname = self._delete_chars(text)

    def _extrac_name(self, data):
        text = self._find_row_by_delta_height(4.5 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        self.name = self._delete_chars(text)

    def _extrac_middle_name(self, data):
        text = self._find_row_by_delta_height(7 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        text = text.lower().replace(' uzbekistan', '').upper()
        self.middle_name = self._delete_chars(text)

    def _extrac_birth_date(self, data):
        text = self._find_row_by_delta_height(10 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        text = text.lower().replace('uzbekistan ', '')
        self.birth_date = self._validate_date(text.replace(' ', '.'))

    def _extrac_gender(self, data):
        text = self._find_row_by_delta_height(13 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        for word in text.split(' '):
            if len(word) == 1:
                if 'M' == word:
                    self.gender = 'Мужской'
                elif 'F' == word:
                    self.gender = 'Женский'

    def _extrac_birth_place(self, data):
        text = self._find_row_by_delta_height(13 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        _birth_place = []
        for word in text.split(' '):
            if len(word) > 1:
                _birth_place.append(word)
        self.birth_place = self._delete_chars(' '.join(_birth_place))

    def _exctrac_issue(self, data):
        text = self._find_row_by_delta_height(15.5 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        _date = text.split(' ')[:3]
        self.issue_date = self._validate_date('.'.join(_date))

    def _extrac_exprition_date(self, data):
        text = self._find_row_by_delta_height(17.5 * self._word_height, data, 2.5 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        _date = text.split(' ')[-3:]
        self.expiration_date = self._validate_date('.'.join(_date))

    def _extrac_authority(self, data):
        text = self._find_row_by_delta_height(15 * self._word_height, data, 3 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        text = text.split(' ')
        if len(text) <= 5:
            _authority = text[3:]
        else:
            _authority = text[3:-3]
        self.authority = self._delete_chars(' '.join(_authority))

    def _extra_extrac(self, data):
        """Extrac data from bottom information"""
        text = self._find_row_by_delta_height(20 * self._word_height, data, 10 * self._word_height,
                                              6 * self._word_height / 7)
        if not text: return
        text = text.replace(' ', '')
        text = [t for t in text.split('<') if t]
        if self.surname is None: self.surname = self._delete_chars(text[1][3:])
        if self.name is None: self.name = self._delete_chars(text[2])
        if self.middle_name is None: self.middle_name = self._delete_chars(' '.join(text[3:5]))
        if self.serial is None or self.number is None: self.parse_serial_number(text[5][:9])
        if self.gender is None:
            if 'm' in text[5][20].lower():
                self.gender = 'Мужской'
            elif 'f' in text[5][20].lower():
                self.gender = 'Женский'

    def extract_data(self, data):
        self._set_coordinate(data)
        self.citizenship = self.get_citizenship()
        if self._word_height is None: return
        # self._extrac_serial_number(data)
        # self._extrac_surname(data)
        # self._extrac_name(data)
        # self._extrac_middle_name(data)
        # self._extrac_gender(data)
        self._extrac_birth_date(data)
        self._extrac_birth_place(data)
        self._exctrac_issue(data)
        self._extrac_exprition_date(data)
        self._extrac_authority(data)
        # Extra extrac
        self._extra_extrac(data)
