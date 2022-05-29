from pathlib import Path
from docrecer.core.logger import logger
from docrecer.core.config import Config
from docrecer.core.image import get_documents_from_image
from docrecer.core.recognizers.base_recognizer import BaseRecognizer
from docrecer.core.ocrs.response import RecognizedData
from docrecer.core.ocrs import image_to_data
from docrecer.converters import pdf2numpy


class PdfRecognizer(BaseRecognizer):
    def recognize(self, config: Config):
        if isinstance(self.source_file, Path) and self.source_file.suffix == '.pdf':
            list_of_doc = self._pdf_to_list_of_docs()
            if config.load_ocr_data:
                data = RecognizedData.load_ocr_data(self.get_ocr_data_path())
            else:
                data = image_to_data(list_of_doc, config)
                if config.save_ocr_data:
                    data.save_ocr_data(self.get_ocr_data_path())
            if data:
                for page in data:
                    self._sort(page)
        else:
            raise ValueError(f'Invalid pdf file {self.source_file}')

    def _pdf_to_list_of_docs(self):
        pages = pdf2numpy(self.source_file)
        logger.debug(f'Converted pdf file {len(pages)} images')
        list_of_doc = []
        for i, image in enumerate(pages):
            for doc in get_documents_from_image(image):
                list_of_doc.append(doc)
        return list_of_doc
