import re
from docrecer.core.base.base_patent import PatentData


class CardPatent(PatentData):
    _is_it_keywords = ['патент']
    _set_coordinate_key = 'Фамилия'

    def _extrac_serial_number(self, data):
        _text = self._find_row_same_word('Серия', data)
        if not _text: return
        _text = _text.split(' ')
        try:
            self.serial = self._delete_chars(_text[0])
        except IndexError:
            pass
        try:
            self.number = self._delete_chars(_text[1])
        except IndexError:
            pass

    def _extrac_surname(self, data):
        _text = self._find_row_same_word('Фамилия', data)
        if not _text: return
        _text = _text.split(' ')
        try:
            self.surname = self._delete_chars(_text[0])
        except IndexError:
            pass

    def _extrac_name(self, data):
        _text = self._find_row_same_word('Имя', data, 1.3 * self._word_height)
        if not _text: return
        _text = _text.split(' ')
        try:
            self.name = self._delete_chars(_text[0])
        except IndexError:
            pass

    def _extrac_middle_name(self, data):
        _text = self._find_row_same_word('Отчество', data, 1.3 * self._word_height)
        if not _text: return
        _text = _text.split(' ')
        self.middle_name = self._delete_chars(_text[0])

    def _extrac_birth_date(self, data):
        _text = self._find_row_same_word('Дата рождения', data)
        if not _text: return
        self.birth_date = self._validate_date(_text.replace(' ', '.').replace(',', '.'))

    def _extrac_citizenship(self, data):
        _text = self._find_row_same_word('Гражданство', data)
        if not _text: return
        _text = _text.split(' ')
        self.citizenship = self._delete_chars(_text[0])

    def _extrac_position(self, data):
        _text = self._find_row_same_word('Профессия', data, word_height=10 * self._word_height)
        if not _text: return
        _text = re.sub(r'\([^()]*\)', '', _text)
        _text = _text[1:] if _text.startswith(' ') else _text
        self.position = self._delete_chars(_text)

    def _extrac_tin(self, data):
        _text = self._find_row_same_word('личност', data, word_height=2 * self._word_height, enter_avaible=True)
        if not _text: return
        for item in _text.split('\n'):
            item = item.replace('/', ' ')
            for word in item.split(' '):
                try:
                    int(word)
                    item = item.replace(' ', '')
                    self.tin = self._delete_chars(item[-12:])
                    self.parse_serial_number_passport(data, item[:-12])
                    break
                except ValueError:
                    pass

    def _extrac_authority(self, data):
        _text = self._find_row_same_word('Кем выдано', data, word_height=4 * self._word_height)
        if not _text: return
        self.authority = self._delete_chars(_text)

    def _extrac_issue_date(self, data):
        _text = self._find_row_same_word('Дата выдачи', data, word_height=4 * self._word_height)
        if not _text: return
        self.issue_date = self._validate_date(_text)

    def extract_data(self, data, config, image):
        # Face side
        try:
            self._set_coordinate(data)
            if self._word_height is not None:
                self._extrac_serial_number(data)
                self._extrac_surname(data)
                self._extrac_name(data)
                self._extrac_middle_name(data)
                self._extrac_birth_date(data)
                self._extrac_citizenship(data)
                self._extrac_position(data)
                self._extrac_tin(data)
            else:
                # Back side
                self._set_coordinate_key = 'Особые'
                self._set_coordinate(data)
                if self._word_height is None: return
                self._extrac_authority(data)
                self._extrac_issue_date(data)
        except IndexError or KeyError:
            pass
