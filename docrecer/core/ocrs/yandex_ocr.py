import base64
import requests
import numpy as np
from PIL import Image
from io import BytesIO

from docrecer.converters import pdf2numpy
from docrecer.core.logger import logger
from .exceptions import YandexOCRError
from .response import RecognizedData, PageData, _Row, _Word, _Point
from .ocr import Ocr

__all__ = ['YandexOcr', 'YandexOCRError']


class YandexOcr(Ocr):
    _request_file_format = 'PDF'
    _request_mime_type = 'application/pdf'
    _request_langs = ['en', 'ru']
    _vision_url = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'

    def image_to_base64(self, image):
        with BytesIO() as buff:
            pil_img = Image.fromarray(image)
            pil_img.save(buff, format=self._request_file_format)
            return base64.b64encode(buff.getvalue()).decode("utf-8")

    def _get_headers(self):
        return {'Authorization': f'Api-Key {self.config.yandex_ocr_api_key}'}

    def _get_body(self, image_as_base64: list):

        data = {'analyzeSpecs': [
            {
                'content': image_as_base64,
                "mime_type": self._request_mime_type,
                'features': [
                    {
                        'type': 'TEXT_DETECTION',
                        'textDetectionConfig': {
                            'languageCodes': self._request_langs,
                        }
                    },
                    {
                        'type': 'TEXT_DETECTION',
                        'textDetectionConfig': {
                            'languageCodes': self._request_langs,
                            'model': 'passport'
                        }
                    }
                ]
            }
        ]}
        return data

    def _divide_two_part(self, content):
        with BytesIO(content.encode('utf-8')) as buf:
            images = pdf2numpy(base64.b64decode(buf.getvalue()))
            logger.debug(f'Dividing 2 parts of {len(images)} images')
            mid = len(images) // 2
            # Content 1
            buf.truncate(0)
            pil_img_list = [Image.fromarray(image) for image in images[:mid]]
            pil_img_list[0].save(buf, self._request_file_format, save_all=True, append_images=pil_img_list[1:])
            content1 = base64.b64encode(buf.getvalue()).decode("utf-8")
            # Content 2
            buf.truncate(0)
            pil_img_list = [Image.fromarray(image) for image in images[mid:]]
            pil_img_list[0].save(buf, self._request_file_format, save_all=True, append_images=pil_img_list[1:])
            content2 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return content1, content2

    def request_to_yandex_api(self, image_as_base64):
        response = requests.post(self._vision_url, headers=self._get_headers(),
                                 json=self._get_body(image_as_base64))
        if response.status_code == 500:
            logger.error(f"{response.text} (status_code: {response.status_code})")
            return []
        elif response.status_code != 200:
            raise YandexOCRError(f"{response.text} (status_code: {response.status_code})")
        return response.json().get('results', [])

    @staticmethod
    def _parse_data(response_data) -> RecognizedData:
        return_data = RecognizedData()
        for result in response_data:
            for r in result['results']:
                try:
                    for p in r['textDetection']['pages']:
                        data = PageData([], '', width=int(p['width']), height=int(p['height']))
                        data_text = []
                        for block in p.get('blocks', []):
                            for block_line in block['lines']:
                                words = block_line['words']
                                row = _Row()
                                for word in words:
                                    _word = _Word()
                                    points = word['boundingBox']['vertices']
                                    for pp in points:
                                        _word.add(_Point(int(pp.get('x', 0)), int(pp.get('y', 0))))
                                    _word.text = word['text']
                                    _word.confidence = float(word['confidence'])
                                    row.add(_word)
                                row.text = ' '.join([w.text for w in row.words])
                                data_text.append(row.text)
                                data.add(row)
                                data.text = '\n'.join(data_text)
                        data.entities = p.get('entities', [])
                        return_data.add(data)
                except KeyError as _exp:
                    logger.warning(f'YandexOCR: {_exp}')
        for i in range(0, len(return_data.pages), 2):
            page = return_data[i]
            next_page = return_data.pages.pop(i + 1)
            page.entities = next_page.entities
        return return_data

    def __call__(self, image: np.array) -> RecognizedData:
        if self.config.yandex_ocr_api_key is None:
            raise YandexOCRError('Yandex OCR API key error: Api key not given')
        images_as_base64 = self.image_to_base64(image)
        results = self.request_to_yandex_api(images_as_base64)
        recognizer_data = self._parse_data(results)
        return self._reorder_recognized_data(recognizer_data)
