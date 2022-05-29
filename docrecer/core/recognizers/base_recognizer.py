import numpy as np
from pathlib import Path
from typing import Union

from docrecer import logger, Config
from docrecer.core.personal import PersonalData
from docrecer.core.ocrs.response import PageData


class BaseRecognizer:
    persanal_data = PersonalData()

    def __init__(self, source_file: Union[Path, str, np.array], output_dir: Union[Path, str] = None):
        self.source_file = Path(source_file) if isinstance(source_file, str) else source_file
        self.output_dir = Path(output_dir) if isinstance(output_dir, str) else output_dir

    def get_output_jsonpath(self):
        if self.output_dir is None:
            raise ValueError(f'output_dir is None')
        filename = Path(self.source_file.parts[-1]).with_suffix('.json')
        return self.output_dir.joinpath(filename)

    def get_ocr_data_path(self):
        if self.output_dir is None:
            raise ValueError(f'output_dir is None')
        filename = Path(self.source_file.parts[-1]).with_suffix('.json')
        return self.output_dir.joinpath(f'ocr_response_{filename}')

    def get_output_path(self):
        if self.output_dir is None:
            raise ValueError(f'output_dir is None')
        return self.output_dir.joinpath(self.source_file.parts[-1])

    def _sort(self, data: PageData):
        if self.persanal_data.passport.is_passport_data(data):
            logger.debug('Load Passport files')
            self.persanal_data.passport.update(**self.persanal_data.passport.load_from_data(data))
        elif self.persanal_data.patent.is_patent_data(data):
            logger.debug('Load Patent files')
            self.persanal_data.patent.update(**self.persanal_data.patent.load_from_data(data))
        elif self.persanal_data.migration_card.is_migration_card_data(data):
            logger.debug('Load Migration card files')
            self.persanal_data.migration_card.update(**self.persanal_data.migration_card.load_from_data(data))
        elif self.persanal_data.snils.is_snils_data(data):
            logger.debug('Load Snils files')
            self.persanal_data.snils.update(**self.persanal_data.snils.load_from_data(data))
        else:
            logger.warning(f'Can not get data from document')

    def recognize(self, config: Config):
        pass
