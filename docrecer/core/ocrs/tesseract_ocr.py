import numpy as np
import pytesseract

from .exceptions import TesseractOCRExeption
from .response import RecognizedData, _Word, _Row, PageData, _Point
from .ocr import Ocr

__all__ = ['TesseractOcr', 'TesseractOCRExeption']


class TesseractOcr(Ocr):

    @staticmethod
    def _parse_data(response_data):
        row, text = _Row(), []
        page = PageData()
        page_text = []
        for i, (x, y, w, h, t, c) in enumerate(zip(response_data['left'], response_data['top'], response_data['width'],
                                                   response_data['height'], response_data['text'],
                                                   response_data['conf'])):
            if c == '-1': continue
            word = _Word()
            p1 = _Point(int(x), int(y))
            p2 = _Point(int(x), int(y) + int(h))
            p3 = _Point(int(x) + int(w), int(y) + int(h))
            p4 = _Point(int(x) + int(w), int(y))
            word.points = [p1, p2, p3, p4]
            word.text = str(t)
            word.confidence = float(c)
            if not row:
                row.add(word)
                text.append(word.text)
            else:
                last_word = row.words[-1]
                l_p1, l_p2, *_ = last_word.points
                if l_p1.y - abs(l_p1.y - l_p2.y) / 2 < p1.y < l_p1.y + abs(l_p1.y - l_p2.y) / 2:
                    row.add(word)
                    text.append(word.text)
                else:
                    text = ' '.join(text)
                    row.text = text
                    page.add(row)
                    page_text.append(text)
                    row, text = _Row([word]), [word.text]
        page.text = '\n'.join(page_text)
        return page

    def __call__(self, images: list[np.array, ...]):
        if self.config.tesseract_cmd is None:
            raise TesseractOCRExeption('Config not given tesseract cmd')

        pytesseract.pytesseract.tesseract_cmd = self.config.tesseract_cmd

        return_data = RecognizedData()
        for image in images:
            data = pytesseract.image_to_data(image, lang=self.config.tesseract_langs,
                                             config=self.config.tesseract_config,
                                             output_type=pytesseract.Output.DICT)
            page = self._parse_data(data)
            page.width = image.shape[1]
            page.height = image.shape[0]
            return_data.add(page)
        return self._reorder_recognized_data(return_data)
