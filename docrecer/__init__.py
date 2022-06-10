import os as _os
import shutil as _shutil
from pathlib import Path as _Path

import numpy as np

from docrecer.core.logger import logger
from docrecer.core.config import Config
from docrecer.core.recognizers.pdf_recognizer import PdfRecognizer
from docrecer.core.recognizers.image_recognizer import ImageRecognizer

__all__ = ['documents_recognizer', 'Config', 'file_recognizer']

logger.bigtext('Document Recognizer')


def documents_recognizer(config: Config):
    # Create folder for results
    if isinstance(config.output_path, str): config.output_path = _Path(config.output_path)
    config.output_path.mkdir()
    logger.debug(f'Maked dir {config.output_path}')
    # Map input path
    for in_path, folders, files in _os.walk(config.input_path):
        in_path = _Path(in_path)
        out_path = _Path(config.output_path)
        # Rename outpath
        for i, part in enumerate(in_path.parts):
            try:
                _part = config.input_path.parts[i]
                if not _part == part:
                    out_path = out_path.joinpath(part)
            except IndexError:
                out_path = out_path.joinpath(part)
        # Mkdir
        for f in folders:
            out_path.joinpath(f).mkdir()
        # Recognize files
        for f in files:
            f = _Path(in_path, f)
            file_recognizer(f, config, out_path)


def file_recognizer(input_path: str or _Path or np.array, config: Config, output_path=None) -> dict:
    if isinstance(input_path, str): input_path = _Path(input_path)
    if output_path is None: output_path = config.output_path

    if isinstance(input_path, _Path) and input_path.suffix == '.pdf':
        logger.debug(f'Working with file: {input_path}')
        pdf_data = PdfRecognizer(input_path, output_path)
        pdf_data.persanal_data.reset()
        pdf_data.recognize(config)
        # Write resualt
        if pdf_data.output_dir:
            pdf_data.persanal_data.save_as_json(pdf_data.get_output_jsonpath())
            _shutil.copy(pdf_data.source_file, pdf_data.get_output_path())
        return pdf_data.persanal_data.to_json()
    elif (isinstance(input_path, _Path) and input_path.suffix in ('.png', '.jpg', '.jpeg')) \
            or isinstance(input_path, np.ndarray):
        image_data = ImageRecognizer(input_path, output_path)
        image_data.persanal_data.reset()
        image_data.recognize(config)
        # Write result
        if image_data.output_dir:
            image_data.persanal_data.save_as_json(image_data.get_output_jsonpath())
            _shutil.copy(image_data.source_file, image_data.get_output_path())
        return image_data.persanal_data.to_json()
    else:
        logger.warning(f'Not supported file {input_path}')
