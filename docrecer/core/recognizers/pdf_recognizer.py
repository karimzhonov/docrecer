from pathlib import Path
from docrecer.core.logger import logger
from docrecer.core.config import Config
from docrecer.core.image import get_documents_from_image
from docrecer.core.recognizers.base_recognizer import BaseRecognizer
from docrecer.core.ocrs.response import RecognizedData
from docrecer.converters import pdf2numpy
from docrecer.core.ocrs.yandex_ocr import YandexOcr


class PdfRecognizer(BaseRecognizer):
    def recognize(self, config: Config):
        if not isinstance(self.source_file, Path) and self.source_file.suffix == '.pdf':
            raise ValueError(f'Invalid pdf file {self.source_file}')

        if config.load_ocr_data:
            data = RecognizedData.load_ocr_data(self.get_ocr_data_path())
        else:
            list_of_doc = self._pdf_to_list_of_docs()
            data = RecognizedData([YandexOcr(config)(doc)[0] for doc in logger.range(list_of_doc, desc='Yandex ocr')])
            if config.save_ocr_data:
                data.save_as_json(self.get_ocr_data_path())
        if data:
            for page in data:
                self._sort(page)

    def _pdf_to_list_of_docs(self):
        pages = pdf2numpy(self.source_file)
        logger.debug(f'Converted pdf file {len(pages)} images')
        list_of_doc = []
        for i, image in enumerate(pages):
            for doc in get_documents_from_image(image):
                list_of_doc.append(doc)
        return list_of_doc
