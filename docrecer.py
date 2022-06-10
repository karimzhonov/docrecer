import os
import json
from typer import Typer, Option

from docrecer.core.logger import logger
from docrecer.core.config import Config
from docrecer.utils import get_datetime_dirname
from docrecer import documents_recognizer, file_recognizer

app = Typer()


@app.command()
def recognize(
        file_path: str = Option(None, help='path to file pdf or photo'),
        config_path: str = Option(None, help='path to config.json'),
        input_path: str = Option(None, help="path to input dir, if not given equel config['input_path']"),
        output_path: str = Option(None, help="path to output dir if not given equel config['output_path']"),
        yandex_ocr_api_key: str = Option(None, help="Api Key for yandex ocr"),
        tesseract_cmd: str = Option(None, help='Path to tesseract.exe'),
        ocr_name: str = Option(None, help='Ocr name (tesseract, yandex)'),
        log_level: int = Option(0, help="0 - ALL, 1 - warning, debug, error, 2 - warning, error, 3 - error")
):
    """
    Document recognizer CLI
    User guide for single file

    # Yandex Ocr

    python docrecer.py --file-path <path_to (pdf or image)> --output-path <path_to_save> --ocr-name yandex --yandex-ocr-api-key <Api key>

    # PyTesseract Ocr (confidence low)

    python docrecer.py --file-path <path_to (pdf or image)> --output-path <path_to_save> --ocr-name tesseract --tesseract_cmd <path_to_tesseract.exe>

    User guide for many files

    # Yandex ocr

    python docrecer.py --input-path <path_to_dir_which_include_images_or_pdf> --output-path <path_to_save> --ocr-name yandex --yandex-ocr-api-key <Api key>

    # PyTesseract Ocr (confidence low)

    python docrecer.py --input-path <path_to_dir_which_include_images_or_pdf> --output-path <path_to_save> --ocr-name tesseract --tesseract_cmd <path_to_tesseract.exe>
    """
    config = {}
    # Read config
    if config_path is not None:
        try:
            config = json.load(open(config_path))
            if not isinstance(config, dict):
                logger.error('Config must be dict')
        except json.JSONDecodeError:
            logger.error('config_path must be json file')
    config = Config(**config)
    # Reset config
    if input_path:
        config.input_path = input_path
    if output_path:
        config.output_path = output_path
    if yandex_ocr_api_key:
        config.yandex_ocr_api_key = yandex_ocr_api_key
    if tesseract_cmd:
        config.tesseract_cmd = tesseract_cmd
    if ocr_name:
        config.ocr_name = ocr_name
    logger.set_level(log_level)

    # Recognize file
    if file_path is not None:
        return file_recognizer(file_path, config)

    # Recognize folder
    if config.input_path is not None and config.output_path is not None:
        config.output_path = os.path.join(config.output_path, get_datetime_dirname())
        documents_recognizer(config)
    else:
        logger.error('input_path and output_path must be given')

if __name__ == '__main__':
    app()
