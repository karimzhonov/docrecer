import json
from pathlib import Path
from dataclasses import dataclass
from ..serializer import Serializer


@dataclass
class RecognizedData(Serializer):
    pages: list = None

    def __iter__(self):
        if self.pages is None: self.pages = []
        return iter(self.pages)

    @classmethod
    def load_ocr_data(cls, path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f'Load ocr File not founded {path}')
        with open(path, 'r') as file:
            pages = json.load(file)
            return cls._parse_data(pages)

    @classmethod
    def _parse_data(cls, pages):
        data = cls([])
        for pa in pages['pages']:
            page = PageData(**pa)
            page.rows = []
            for r in pa['rows']:
                row = _Row(**r)
                row.words = []
                for w in r['words']:
                    word = _Word(text=w['text'], confidence=float(w['confidence']))
                    word.points = []
                    for p in w['points']:
                        word.points.append(_Point(**p))
                    row.words.append(word)
                page.rows.append(row)
            data.pages.append(page)
        return data

    def add(self, obj):
        if self.pages is None:
            self.pages = []
        self.pages.append(obj)

    def __len__(self):
        return 0 if self.pages is None else len(self.pages)

    def __getitem__(self, item):
        return self.pages[item]


@dataclass
class _Point(Serializer):
    x: int = None
    y: int = None


@dataclass
class _Word(Serializer):
    points: list[_Point, _Point, _Point, _Point] = None
    text: str = ''
    confidence: float = None

    def add(self, obj):
        if self.points is None:
            self.points = []
        self.points.append(obj)

    def __len__(self):
        return 0 if self.points is None else len(self.points)

    def __getitem__(self, item):
        return self.points[item]


@dataclass
class _Row(Serializer):
    words: list[_Word] = None
    text: str = ''

    def add(self, obj):
        if self.words is None:
            self.words = []
        self.words.append(obj)

    def __len__(self):
        return 0 if self.words is None else len(self.words)

    def __getitem__(self, item):
        return self.words[item]


@dataclass
class PageData(Serializer):
    rows: list[_Row] = None
    text: str = ''
    width: int = 0
    height: int = 0
    entities: list = None

    def add(self, obj):
        if self.rows is None:
            self.rows = []
        self.rows.append(obj)

    def __len__(self):
        return 0 if self.rows is None else len(self.rows)

    def __getitem__(self, item):
        return self.rows[item]
