from docrecer.core.base.base_snils import SnilsData


class CardSnils(SnilsData):
    _is_it_keywords = ['страховое']
    _set_coordinate_key = 'страховое'

    def _extrac_number(self, data):
        _text = self._find_row_same_word('обязательного пенсионного страхования', data,
                                         word_height=2 * self._word_height)
        if not _text: return
        self.number = self._delete_chars(_text)

    def extract_data(self, data):
        self._set_coordinate(data)
        if self._word_height is None: return
        self._extrac_number(data)
