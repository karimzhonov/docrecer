from pathlib import Path
from dataclasses import dataclass
from docrecer.core.serializer import Serializer
from docrecer.conf import OCRS


@dataclass
class Config(Serializer):
    def __init__(self,
                 input_path: Path or str = None,
                 output_path: Path or str = None,
                 yandex_ocr_api_key: str = None,
                 tesseract_cmd: Path or str = None,
                 tesseract_config: str = '',
                 tesseract_langs: str = None,
                 ocr_name: OCRS or str = None,
                 load_ocr_data: bool = False,
                 save_ocr_data: bool = True, **kwargs):
        self.input_path = Path(input_path) if isinstance(input_path, str) else input_path
        self.output_path = Path(output_path) if isinstance(output_path, str) else output_path
        self.yandex_ocr_api_key = yandex_ocr_api_key
        self.tesseract_config = tesseract_config
        self.tesseract_langs = tesseract_langs
        self.tesseract_cmd = Path(tesseract_cmd) if isinstance(tesseract_cmd, str) else tesseract_cmd
        self.ocr_name = OCRS(ocr_name) if ocr_name is not None else ocr_name
        self.load_ocr_data = load_ocr_data
        self.save_ocr_data = save_ocr_data
