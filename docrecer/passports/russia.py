from docrecer.core.base.base_passport import PassportData

class RussianPassport(PassportData):
    _is_it_keywords = ['росси']
    _set_coordinate_key = 'росси'

    @staticmethod
    def get_citizenship():
        return "Рассия"

    def parse_serial_number(self, text):
        if len(text) == 10:
            self.serial = self._delete_chars(text[:4])
            self.number = self._delete_chars(text[4:])

    def extract_data(self, data):
        PassportData.extract_data(self, data)

