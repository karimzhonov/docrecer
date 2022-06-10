from .yandex_ocr import YandexOcr
from .tesseract_ocr import TesseractOcr
from docrecer.conf import OCRS


def image_to_data(images, config, model = None):
    if config.ocr_name == OCRS.YANDEX:
        return YandexOcr(config)(images, model)
    elif config.ocr_name == OCRS.TESSERACT:
        return TesseractOcr(config)(images)
