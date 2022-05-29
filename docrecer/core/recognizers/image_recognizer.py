import cv2
from pathlib import Path
from docrecer.core.ocrs.response import RecognizedData
from docrecer.core.recognizers.base_recognizer import BaseRecognizer
from docrecer.core.image import get_documents_from_image
from docrecer.core.ocrs import image_to_data


class ImageRecognizer(BaseRecognizer):
    def recognize(self, config):
        image = self.source_file
        if isinstance(self.source_file, Path):
            image = cv2.imread(self.source_file)
        docs = get_documents_from_image(image)
        if config.load_ocr_data:
            data = RecognizedData.load_ocr_data()
        else:
            data = image_to_data(docs, config)
            data.save_ocr_data()
        if data.pages:
            self._sort(data.pages[0])
