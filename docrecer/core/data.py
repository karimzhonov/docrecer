from datetime import datetime

from docrecer.core.serializer import Serializer
from docrecer.utils import is_include, import_class


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
            if isinstance(value, Data):
                getattr(self, key).update(**value.to_json())
            if value is not None:
                setattr(self, key, value)

    def reset(self):
        for key, value in self.to_json().items():
            setattr(self, key, None)

    @staticmethod
    def _delete_chars(text: str, chars='!@#$%^&*()`~[]{}№«'):
        for char in chars:
            text = text.replace(char, '')
        return text.capitalize()

    @classmethod
    def load_from_data(cls, data):
        instance = cls()
        for _class_path in cls._support_classes:
            _class = import_class(_class_path)
            if getattr(_class, 'is_it')(data):
                instance = _class()
                instance.extract_data(data)
                return instance.to_json()
        return instance.to_json()

    @classmethod
    def is_it(cls, data):
        return is_include(cls._is_it_keywords, data.text)

    def extract_data(self, data):
        pass

    @staticmethod
    def _get_word_coordinate(word, data):
        for item in data.rows:
            if is_include([word], item.text):
                return item.words[0].points[0]

    def _find_row_same_word(self, word, data, word_height=None, min_height=None):
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
                    if not is_include(word.split(' '), _word.text):
                        if min_height is not None:
                            if abs(w_p1.y - w_p2.y) >= min_height:
                                _text.append(_word.text)
                        else:
                            _text.append(_word.text)
        _text = ' '.join(_text)
        _text = _text[1:] if _text.startswith(' ') else _text
        return _text

    def _validate_date(self, text):
        text = text[:-1] if text.endswith('.') else text
        try:
            return self._delete_chars(str(datetime.strptime(text, '%d.%m.%Y').date()))
        except ValueError:
            return None

    def _validate_number(self, text):
        try:
            return self._delete_chars(str(int(text)))
        except ValueError:
            pass

    def _find_row_by_delta_height(self, delta_height, data, word_height: int = None, min_height=None):
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

        return ' '.join(_text)


def is_other_document(data):
    keywords = (
        'чек', 'платеж', 'плательщик', 'перевод', 'опись', 'расписка', 'уведомлен', 'visas', 'viza', 'владелец',
        'гражданина', 'this', 'анкета', 'анкеты', 'соискателя', 'работник', 'заполнить', 'полис', 'ЗАЯВЛЕНИЕ')
    return is_include(keywords, data.text)
