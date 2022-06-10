from docrecer.core.base.base_migration_card import MigrationCardData
from docrecer.core.ocrs.response import PageData


class PaperMigrationCard(MigrationCardData):
    _is_it_keywords = ['migrat']
    _set_coordinate_key = 'Departure'

    def _extrac_serial_number(self, data: PageData):
        _text = self._find_row_same_word('Миграционная карта', data, word_height=4 * self._word_height)
        if not _text: return
        _serial_number = []
        for word in _text.split(' '):
            try:
                int(word)
                _serial_number.append(word)
            except ValueError:
                pass
        _serial_number = ''.join(_serial_number)
        self.serial = self._delete_chars(_serial_number[:4])
        self.number = self._delete_chars(_serial_number[4:])

    def extract_data(self, data, config, image):
        self._set_coordinate(data)
        if self._word_height is None: return
        self._extrac_serial_number(data)
