import cv2
from pathlib import Path
from docrecer.core.ocrs.response import RecognizedData
from docrecer.core.recognizers.base_recognizer import BaseRecognizer
from docrecer.core.image import get_documents_from_image
from docrecer.core.ocrs.yandex_ocr import YandexOcr
from docrecer.core.logger import logger


class ImageRecognizer(BaseRecognizer):
    def recognize(self, config):
        image = self.source_file
        if isinstance(self.source_file, Path):
            image = cv2.imread(self.source_file)
        docs = get_documents_from_image(image)
        if config.load_ocr_data:
            data = RecognizedData.load_ocr_data(self.get_ocr_data_path())
        else:
            data = RecognizedData([YandexOcr(config)(doc)[0] for doc in logger.range(docs, desc='Yandex ocr')])
            if config.save_ocr_data:
                data.save_as_json(self.get_ocr_data_path())
        if data.pages:
            self._sort(data.pages[0])
