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

    def _extrac_serial_number(self, data):
        text = self._find_row_by_delta_height(2 * self._word_height, data)
        if not text: return
        self.parse_serial_number(text)

    def _extrac_surname(self, data):
        text = self._find_row_by_delta_height(4 * self._word_height, data)
        if not text: return
        self.surname = self._delete_chars(text)

    def _extrac_name(self, data):
        text = self._find_row_by_delta_height(7 * self._word_height, data, 1.5 * self._word_height)
        if not text: return
        text = text.replace('Номер', '').replace('номи', '').replace('Name', '').replace('падар', '').replace('/', '')
        _words = text.split(' ')
        __words = []
        for w in _words:
            if len(w) > 0:
                __words.append(w)

        if len(__words) == 2:
            self.name = self._delete_chars(__words[0])
            self.middle_name = self._delete_chars(__words[1])
        else:
            self.name = self._delete_chars(' '.join(__words))

    def _extrac_birth_date(self, data):
        text = self._find_row_by_delta_height(12 * self._word_height, data, 1.5 * self._word_height)
        if not text: return
        words = text.split(' ')
        self.birth_date = self._validate_date(words[0])

    def _exctrac_issue_and_exprition_date(self, data):
        text = self._find_row_by_delta_height(14 * self._word_height, data, 1.5 * self._word_height)
        if not text: return
        words = text.split(' ')
        self.issue_date = self._validate_date(words[0])
        self.expiration_date = self._validate_date(words[1])

    def _extrac_authority(self, data):
        text = self._find_row_by_delta_height(17 * self._word_height, data)
        if not text: return
        self.authority = self._delete_chars(text)

    def _extra_extrac(self, data):
        text = self._find_row_by_delta_height(19 * self._word_height, data, 10*self._word_height)
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

    def extract_data(self, data):
        self._set_coordinate(data)
        self.citizenship = self.get_citizenship()
        if self._word_height is None: return
        # self._extrac_serial_number(data)
        # self._extrac_surname(data)
        # self._extrac_name(data)
        self._extrac_birth_date(data)
        self._exctrac_issue_and_exprition_date(data)
        self._extrac_authority(data)
        self._extra_extrac(data)
