from datetime import datetime

from .serializer import Serializer
from ..utils import is_include, import_class
from .logger import logger


class Data(Serializer):
    _top = 0
    _left = 0
    _word_height = None
    _support_classes = []
    _is_it_keywords = []
    _set_coordinate_key = None
    _save_pickle_path = None

    def _set_coordinate(self, data):
        _data = []
        for item in data.rows:
            if self._set_coordinate_key is not None and is_include([self._set_coordinate_key], item.text):
                p1, p2, p3, p4 = item.words[0].points
                _data.append((p1, p2))
        if not _data: return
        max_coor = _data[0]
        for p1, p2 in _data:
            if abs(p1.y - p2.y) > abs(max_coor[0].y - max_coor[1].y):
                max_coor = p1, p2

        p1, p2 = max_coor
        self._word_height = abs(p1.y - p2.y)
        self._top = p1.y - self._word_height / 2
        self._left = p1.x - self._word_height

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, Serializer):
                getattr(self, key).update(**value.to_json())
            if value:
                setattr(self, key, value)

    def reset(self):
        for key, value in self.to_json().items():
            setattr(self, key, None)

    @staticmethod
    def _delete_chars(text: str, chars='!@#$%^&*()`~[]{}№«'):
        text = text[1:] if text.startswith(' ') else text
        for char in chars:
            text = text.replace(char, '')
        return text.capitalize()

    @classmethod
    def load_from_data(cls, data, config, image):
        instance = cls()
        for _class_path in cls._support_classes:
            _class = import_class(_class_path)
            if getattr(_class, 'is_it')(data):
                instance = _class()
                instance.extract_data(data, config, image)
                return instance.to_json()
        return instance.to_json()

    @classmethod
    def is_it(cls, data):
        return is_include(cls._is_it_keywords, ''.join(data.text.split(' ')))

    def extract_data(self, data, config, image):
        pass

    @staticmethod
    def _get_word_coordinate(word, data):
        for item in data.rows:
            if is_include([word], item.text):
                return item.words[0].points[0]

    def _find_row_same_word(self, word, data, word_height=None, min_height=None,
                            enter_avaible=False, include_word=False):
        """Find text in one area with word"""
        if word_height is None: word_height = self._word_height
        p1 = self._get_word_coordinate(word, data)
        if p1 is None: return []
        _y = p1.y - self._word_height / 3
        _text = []
        for row in data.rows:
            for _word in row.words:
                w_p1, w_p2, *_ = _word.points
                if _y <= w_p1.y <= _y + word_height:
                    if include_word:
                        if min_height is not None:
                            if abs(w_p1.y - w_p2.y) >= min_height:
                                _text.append(_word.text)
                        else:
                            _text.append(_word.text)
                    else:
                        if not is_include(word.split(' '), _word.text):
                            if min_height is not None:
                                if abs(w_p1.y - w_p2.y) >= min_height:
                                    _text.append(_word.text)
                            else:
                                _text.append(_word.text)
            if _text and enter_avaible: _text[-1] += '\n'
        _text = ' '.join(_text)
        _text = _text[1:] if _text.startswith(' ') else _text
        return _text
    @staticmethod
    def _get_all_text(data, min_height=None, enter_avaible = None):
        _text = []
        for row in data.rows:
            for _word in row.words:
                w_p1, w_p2, *_ = _word.points
                if min_height is not None:
                    if abs(w_p1.y - w_p2.y) >= min_height:
                        _text.append(_word.text)
                else:
                    _text.append(_word.text)
            if _text and enter_avaible: _text[-1] += '\n'
        _text = ' '.join(_text)
        _text = _text[1:] if _text.startswith(' ') else _text
        return _text

    def _validate_date(self, text: str, patern='%d.%m.%Y'):
        text = text[1:] if text.startswith(' ') else text
        text = text[:-1] if text.endswith('.') else text
        text = text.replace(' ', '.').replace(',', '.')
        try:
            return self._delete_chars(str(datetime.strptime(text, patern).date().strftime('%d.%m.%Y')))
        except ValueError as _exp:
            return None

    def _validate_number(self, text):
        text = text[1:] if text.startswith(' ') else text
        try:
            return self._delete_chars(str(int(text)))
        except ValueError:
            pass

    @staticmethod
    def _validate_gender(text, mf='mf'):
        if mf[0] in text.lower():
            return 'Мужской'
        elif mf[1] in text.lower():
            return 'Женский'

    def _find_row_by_delta_height(self, delta_height, data, word_height: int = None, min_height=None,
                                  enter_avaible=False):
        """
        Find text by delta height from self._top
        word_height - height of area where extrac text
        min_height - min word height
        """
        if word_height is None: word_height = self._word_height
        _text = []
        _y = self._top + delta_height
        for item in data.rows:
            for word in item.words:
                p1, p2, p3, p4 = word.points
                if _y <= p1.y <= _y + word_height:
                    if min_height is not None:
                        if abs(p1.y - p2.y) >= min_height:
                            _text.append(word.text)
                    else:
                        _text.append(word.text)
            if enter_avaible and _text:
                _text[-1] += '\n'
        return ' '.join(_text)


def is_other_document(data):
    keywords = (
        'чек', 'платеж', 'плательщик', 'перевод', 'опись', 'расписка', 'уведомлен', 'visas', 'viza', 'владелец',
        'гражданина', 'анкета', 'анкеты', 'соискателя', 'работник', 'заполнить', 'полис', 'ЗАЯВЛЕНИЕ', 'банк')
    return is_include(keywords, data.text)
