import datetime
from tqdm import tqdm
import art


class Logger:
    DEBUG = True
    ERROR = True
    WARNING = True
    INFO = True

    @staticmethod
    def _datetime():
        return str(datetime.datetime.now()).split('.')[0]

    def _format(self, mode, msg):
        return f'[{mode}] - {self._datetime()} - {msg}'

    def debug(self, text, end='\n', file=None):
        if self.DEBUG:
            print(self._format('DEBUG', text), end=end, file=file)

    def error(self, text, end='\n', file=None):
        if self.ERROR:
            print(self._format('ERROR', text), end=end, file=file)

    def info(self, text, end='\n', file=None):
        if self.INFO:
            print(self._format('INFO', text), end=end, file=file)
    def warning(self, text, end='\n', file=None):
        if self.WARNING:
            print(self._format('WARNING', text), end=end, file=file)

    def set_level(self, level: int):
        """0 - ALL, 1 - warning, debug, error, 2 - warning, error, 3 - error"""
        if level == 1:
            self.INFO = False
            self.DEBUG = True
            self.WARNING = True
            self.ERROR = True
        elif level == 2:
            self.INFO = False
            self.DEBUG = False
            self.WARNING = True
            self.ERROR = True
        elif level == 3:
            self.INFO = False
            self.DEBUG = False
            self.WARNING = False
            self.ERROR = True
        else:
            self.INFO = True
            self.DEBUG = True
            self.WARNING = True
            self.ERROR = True

    def range(self, __iter, desc = ''):
        if self.DEBUG:
            return tqdm(__iter, desc=self._format('DEBUG', desc))

    def bigtext(self, text, font=art.DEFAULT_FONT, sep = '\n'):
        if self.INFO:
            result = art.text2art(text, font, sep=sep)
            print(result)

logger = Logger()
