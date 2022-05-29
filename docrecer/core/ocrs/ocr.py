from docrecer.core.config import Config
from .response import RecognizedData, PageData


class Ocr:
    def __init__(self, config: Config = None):
        if config is None: config = Config()
        self.config = config

    @staticmethod
    def __reorder_page_data(page_data: PageData, mode: str):
        """mode = up, down, left"""
        height, width = page_data.height, page_data.width

        for item in page_data.rows:
            for word in item.words:
                for point in word.points:
                    if mode == 'up':
                        point.x, point.y = height - point.y, point.x
                    elif mode == 'down':
                        point.x, point.y = point.y, width - point.x
                    elif mode == 'left':
                        point.x, point.y = width - point.x, height - point.y
        return page_data

    def _reorder_recognized_data(self, data: RecognizedData):
        for page in data:
            w1_p1, w1_p2 = 0, 0,
            w2_p1, w2_p2 = 0, 0
            for item in page.rows:
                try:
                    w1_p1, w1_p2, *_ = item.words[0].points
                    w2_p1, w2_p2, *_ = item.words[1].points
                    break
                except IndexError:
                    pass
            # If words not founded
            if w1_p1 == 0 or w2_p1 == 0: continue
            # Checkiing rotate
            if abs(w1_p1.y - w2_p1.y) < 10:
                # ---
                if w1_p1.x > w2_p1.x:
                    # to left
                    self.__reorder_page_data(page, 'left')
            else:
                # |
                if w1_p1.y > w2_p1.y:
                    # Up
                    self.__reorder_page_data(page, 'up')
                else:
                    # Down
                    self.__reorder_page_data(page, 'down')
        return data