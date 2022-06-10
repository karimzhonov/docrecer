import cv2.cv2 as cv2
import numpy as np
from typer import Typer, Option
from docrecer.core.logger import logger
from docrecer.core.networks.clasificator import DocumentClasificator
from docrecer.core.networks.dataset import load_dataset

app = Typer()


@app.command()
def train(dataset_path: str = Option(None, help='Path to folder with photos')):
    if dataset_path is None:
        logger.error('Train path must be given')
        return
    model = DocumentClasificator()
    x_train, y_train = load_dataset(dataset_path)
    model.train(x_train, y_train, summery=True, workers=6, epochs=10)


@app.command()
def test(dataset_path: str = Option(None, help='Path to folder with photos')):
    if dataset_path is None:
        logger.error('Train path must be given')
        return
    model = DocumentClasificator()
    model.load()
    x_train, y_train = load_dataset(dataset_path)
    predicts = model.predicts(x_train)

    mask = [1 for p, y in zip(predicts, y_train) if model.word_index[p] == y]
    logger.info(f'Accuracy: {sum(mask) / len(x_train)}')


@app.command()
def predict(dataset_path: str = Option(None, help='Path to folder with photos')):
    if dataset_path is None:
        logger.error('Train path must be given')
        return
    model = DocumentClasificator()
    model.load()
    x_train, y_train = load_dataset(dataset_path)
    y_train_cat = DocumentClasificator().refacrtor_y_train(y_train)
    for y, x, yc in zip(y_train, x_train, y_train_cat):
        p = model.predict(x)
        if not model.word_index[p] == y:
            logger.info(f'Model predict - {model.word_index[p]}')
            logger.info(f'True answer - {y} - {model.word_index[np.argmax(yc)]}')
            cv2.imshow('Result', x)
            cv2.waitKey(0)


if __name__ == '__main__':
    app()
