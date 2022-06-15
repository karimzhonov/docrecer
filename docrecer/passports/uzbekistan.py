from docrecer.core.base.base_passport import PassportData


class UzbekistanInternationalPassport(PassportData):
    _is_it_keywords = ['Uzbekistan']
    _set_coordinate_key = 'PASSPORT'

    def get_citizenship(self, data):
        return 'Узбекистан'

    def parse_serial_number(self, text):
        for word in text.split(' '):
            if len(word) == 9:
                _number = self._validate_number(word[2:])
                if _number is not None:
                    self.number = _number
                    self.serial = word[:2]

    def extract_data(self, data, config, image):
        config.yandex_ocr_langs.append('uz')
        PassportData.extract_data(self, data, config, image)
        config.yandex_ocr_langs.pop()
        if self.citizenship:
            if self._word_height is None: return
            # Extrac data from bottom
            text = self._find_row_by_delta_height(18.5 * self._word_height, data, 10 * self._word_height,
                                                  6 * self._word_height / 7)
            try:
                if text:
                    text = text.replace(' ', '')
                    text = [t for t in text.split('<') if t]
                    if not self.name: self.name = self._delete_chars(text[2])
                    if not self.surname: self.surname = self._delete_chars(text[1][3:])
                    if not self.middle_name: self.middle_name = self._delete_chars(' '.join(text[3:5]))
                    if not self.serial or not self.number: self.parse_serial_number(text[5][:9])
                    if not self.gender: self.gender = self._validate_gender(text[5])
            except Exception:
                pass
            # Extrac Authory
            if not self.authority:
                text = self._find_row_by_delta_height(15.5 * self._word_height, data, 3 * self._word_height,
                                                      6 * self._word_height / 7)
                try:
                    if text:
                        text = text.split(' ')
                        for i, word in enumerate(text):
                            try:
                                int(word)
                            except ValueError:
                                self.authority = self._delete_chars(f'{word} {text[i + 1]}')
                except Exception:
                    pass
            # extrac surname
            if not self.surname:
                text = self._find_row_by_delta_height(1.5 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text: self.surname = self._delete_chars(text)
            # extrac name
            if not self.name:
                text = self._find_row_by_delta_height(3.5 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text: self.name = self._delete_chars(text)
            # extrac middle name
            if not self.middle_name:
                text = self._find_row_by_delta_height(5 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text: self.middle_name = self._delete_chars(text.lower().replace(' uzbekistan', '').upper())
            # extrac birth date
            if not self.birth_date:
                text = self._find_row_by_delta_height(8 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text: self.birth_date = self._validate_date(
                    text.lower().replace('uzbekistan ', '').replace(' ', '.'))
            # extrac birth place
            if not self.birth_place:
                text = self._find_row_by_delta_height(11 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text:
                    _birth_place = []
                    for word in text.split(' '):
                        if len(word) > 1:
                            _birth_place.append(word)
                    self.birth_place = self._delete_chars(' '.join(_birth_place))
            # extrac issue date
            if not self.issue_date:
                text = self._find_row_by_delta_height(13.5 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text: self.issue_date = self._validate_date('.'.join(text.split(' ')[:3]))
            # extrac expiration_date
            if not self.expiration_date:
                text = self._find_row_by_delta_height(15.5 * self._word_height, data, 2.5 * self._word_height,
                                                      6 * self._word_height / 7)
                if text: self.expiration_date = self._validate_date('.'.join(text.split(' ')[-3:]))
