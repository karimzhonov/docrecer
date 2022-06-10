from docrecer.core.base.base_passport import PassportData


class RussianPassport(PassportData):
    _is_it_keywords = ['росси', 'Личный']
    _set_coordinate_key = 'росси'

    def get_citizenship(self, data):
        return "Рассия"

    def parse_serial_number(self, text):
        if len(text) == 10:
            self.serial = self._validate_number(text[:4])
            self.number = self._validate_number(text[4:])

    def extract_data(self, data, config, image):
        PassportData.extract_data(self, data, config, image)
