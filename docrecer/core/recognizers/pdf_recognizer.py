from pathlib import Path
from ..logger import logger
from ..config import Config
from ..image import get_documents_from_image
from ..recognizers.base_recognizer import BaseRecognizer
from ..ocrs.response import RecognizedData
from ..ocrs import image_to_data
from ...converters import pdf2numpy


class PdfRecognizer(BaseRecognizer):
    def recognize(self, config: Config):
        if not isinstance(self.source_file, Path) and self.source_file.suffix == '.pdf':
            raise ValueError(f'Invalid pdf file {self.source_file}')
        list_of_doc = self._pdf_to_list_of_docs()
        if config.load_ocr_data:
            data = RecognizedData.load_ocr_data(self.get_ocr_data_path())
        else:
            data = image_to_data(list_of_doc, config)
        if data:
            for page, image in zip(data, list_of_doc):
                self._sort(page, config, image)
        if config.save_ocr_data:
            data.save_as_json(self.get_ocr_data_path())

    def _pdf_to_list_of_docs(self):
        pages = pdf2numpy(self.source_file)
        logger.debug(f'Converted pdf file {len(pages)} images')
        list_of_doc = []
        for i, image in enumerate(pages):
            for doc in get_documents_from_image(image):
                list_of_doc.append(doc)
        return list_of_doc