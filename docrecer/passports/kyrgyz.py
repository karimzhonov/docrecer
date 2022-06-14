import re
from datetime import datetime
from docrecer.core.base.base_passport import PassportData
from docrecer.utils import is_include


class KyrgyzPassport(PassportData):
    _is_it_keywords = ['кыргыз', 'kgz']
    _set_coordinate_key = 'kyrgyz republic'

    def get_citizenship(self, data):
        return "Кыргызтан"

    def parse_serial_number(self, text):
        if len(text) == 9:
            self.serial = self._delete_chars(text[:2])
            self.number = self._validate_number(text[2:])

    def _extrac_paper_passport(self, data):
        self._set_coordinate_key = 'kyrgyz republic'
        self._set_coordinate(data)
        text = self._find_row_same_word(self._set_coordinate_key, data,
                                        50 * self._word_height, 6 * self._word_height / 7, True)
        text = [t for t in text.split('\n') if t]
        # Extrac all date
        _date = []
        for item in text[:-2]:
            _date = [*re.findall(r'\d\d\s\d\d\s\d\d\d\d', item),
                    *[f'{d[:2]} {d[2:4]} {d[4:]}' for d in re.findall(r'[0-9]+', item) if len(d) == 8],
                    *_date]
        _date = sorted(_date, key= lambda k: datetime.strptime(k, '%d %m %Y'))
        if not self.birth_date: self.birth_date = self._validate_date(_date[0])
        if not self.issue_date: self.issue_date = self._validate_date(_date[1])
        if not self.expiration_date: self.expiration_date = self._validate_date(_date[2])
        # Extrac bottom
        if not self.surname: self.surname = self._delete_chars(text[-2].split('<<')[0][6:].replace('<', ' '))
        if not self.name: self.name = self._delete_chars(text[-2].split('<<')[1].replace('<', ' '))
        if (not self.serial) or (not self.number):
            self.parse_serial_number(self._delete_chars(text[-1].lower().split('kgz')[0][:10]))
        if not self.gender: self.gender = self._validate_gender(text[-1].lower().split('kgz')[1])
        if not self.birth_place: self.birth_place = self.get_citizenship(data)

    def _extrac_card_passport(self, data):
        if is_include(['card'], data.text):
            # first type card passport
            pass
        else:
            # second type card passport
            self._set_coordinate_key = 'паспорт'
            if is_include([self._set_coordinate_key], data.text):
                # front
                self._set_coordinate(data)
                text = self._find_row_same_word('паспорт', data, 25 * self._word_height, 6 * self._word_height / 7,
                                                True)
                text = [t for t in text.split('\n') if t]
                if len(text) == 9:
                    if not self.middle_name: self.middle_name = self._delete_chars(text.pop(2))
                if not self.surname: self.surname = self._delete_chars(text[0])
                if not self.name: self.name = self._delete_chars(text[1])
                if not self.birth_date: self.birth_date = self._validate_date(text[2])
                if (not self.serial) or (not self.number): self.parse_serial_number(self._delete_chars(text[5]))
                if not self.gender: self.gender = self._validate_gender(text[3], 'эа')
            else:
                # back
                self._set_coordinate_key = 'kgz'
                self._set_coordinate(data)
                text = self._get_all_text(data, 4 * self._word_height / 7, True)
                text = [t for t in text.split('\n') if t]
                if len(text) == 9:
                    text[1] += text.pop(2)
                if not self.birth_place: self.birth_place = self._delete_chars(text[1])
                if not self.issue_date: self.issue_date = self._validate_date(text[2])
                if not self.expiration_date: self.expiration_date = self._validate_date(text[3])
                if not self.authority: self.authority = self._delete_chars(text[4])
                # extrac bottom item
                _bottom = ''.join(text[-3:]).replace(' ', '').replace('«', '<').split('<')
                _bottom = [t for t in _bottom if t]
                if (not self.serial) or (not self.number): self.parse_serial_number(self._delete_chars(_bottom[0][5:14]))
                if not self.gender: self.gender = self._validate_gender(_bottom[1])
                _bottom = text[-1].replace(' ', '').replace('«', '<').split('<<')
                _bottom = [t for t in _bottom if t]
                if not self.surname: self.surname = self._delete_chars(_bottom[0].replace('<', ' '))
                if not self.name: self.name = self._delete_chars(_bottom[1].replace('<', ' '))


    def extract_data(self, data, config, image):
        config.yandex_ocr_langs.append('ky')
        PassportData.extract_data(self, data, config, image)
        if is_include(['P<KGZ'], data.text):
            self._extrac_paper_passport(data)
        else:
            self._extrac_card_passport(data)
