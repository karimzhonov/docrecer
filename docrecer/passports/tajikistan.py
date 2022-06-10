from docrecer.core.base.base_passport import PassportData
from docrecer.utils import is_include


class TajikistanPasport(PassportData):
    _is_it_keywords = ['Чумхурии', 'Точикистон', 'Tajikistan']
    _set_coordinate_key = 'Republic of Tajikistan'

    def get_citizenship(self, data):
        return 'Таджикистан'

    def parse_serial_number(self, text):
        for word in text.split(' '):
            if self._validate_number(word) is not None:
                self.number = self._validate_number(word)

    def extract_data(self, data, config, image):
        config.yandex_ocr_langs.append('tg')
        PassportData.extract_data(self, data, config, image)
        config.yandex_ocr_langs.pop()
        if self.citizenship:
            self.extrac_with_text(data)

    def extrac_with_text(self, data):
        for i, row in enumerate(data):
            if is_include(['tjk'], row.text):
                if not self.number: self.parse_serial_number(data[i + 1].text)
                if not self.surname: self.surname = self._delete_chars(data[i + 3].text)
                if not self.name: self.name = self._delete_chars(data[i + 5].text.split(' ')[0])
                if not self.middle_name: self.middle_name = self._delete_chars(data[i + 5].text.split(' ')[1])
                if not self.birth_date: self.birth_date = self._validate_date(data[i + 8].text.split(' ')[0])
                if not self.gender: self.gender = self._validate_gender(data[i + 8].text.split(' ')[1])
                if not self.issue_date: self.issue_date = self._validate_date(data[i + 9].text.split(' ')[0])
                if not self.expiration_date: self.expiration_date = self._validate_date(data[i + 9].text.split(' ')[1])
                if not self.authority: self.authority = self._delete_chars(data[i + 11].text)
                break

    def extrac_with_coordinate(self, data):
        if self._word_height is None: return
        # Extrac bottom
        text = self._find_row_by_delta_height(22 * self._word_height, data, 10 * self._word_height)
        if text:
            text = text.replace(' ', '<').replace('«', '<')
            text = [t for t in text.split('<') if t]

            if not self.surname: self.surname = self._delete_chars(text[1][3:])
            if not self.name: self.name = self._delete_chars(text[2])
            if not self.number: self.parse_serial_number(text[3][:9])
            if not self.gender:
                if 'm' in text[3][20].lower():
                    self.gender = 'Male'
                elif 'f' in text[3][20].lower():
                    self.gender = 'Female'
        # extrac authority
        if not self.authority:
            _authority = []
            text = self._find_row_by_delta_height(16 * self._word_height, data, 2 * self._word_height,
                                                  enter_avaible=True)
            for item in text.split('\n'):
                if item.startswith(' '): item = item[1:]
                if not self._validate_date(item) and item:
                    _authority.append(item)
            self.authority = '\n'.join(_authority)
        # extrac birth date
        if not self.birth_date:
            text = self._find_row_by_delta_height(14 * self._word_height, data, 1.5 * self._word_height)
            if text:
                words = text.split(' ')
                self.birth_date = self._validate_date(words[0])
        # extrac surname
        if not self.surname:
            text = self._find_row_by_delta_height(6 * self._word_height, data)
            if text:
                text = text.replace('Шиноснома', '').replace('passport', '').replace('/', '')
                self.surname = self._delete_chars(text)
        # extrac name
        if not self.name:
            text = self._find_row_by_delta_height(9 * self._word_height, data, 1.5 * self._word_height)
            if text:
                text = text.replace('Номер', '').replace('номи', '').replace('Name', ''). \
                    replace('падар', '').replace('/', '')
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
        # extrac issue and expiration date
        if (not self.issue_date) or (not self.expiration_date):
            text = self._find_row_by_delta_height(16 * self._word_height, data, 1.5 * self._word_height)
            if text:
                words = text.split(' ')
                self.issue_date = self._validate_date(words[0])
                self.expiration_date = self._validate_date(words[1])
