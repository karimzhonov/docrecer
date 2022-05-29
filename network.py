from typer import Typer, Option
from docrecer.core.logger import logger
from docrecer.core.networks.clasificator import DocumentClasificator
from docrecer.core.networks.dataset import load_dataset

app = Typer()


@app.command()
def train(train_path: str = Option(None, help='Path to folder with photos')):
    if train_path is None:
        logger.error('Train path must be given')
        return
    model = DocumentClasificator()
    x_train, y_train = load_dataset(train_path)
    model.train(x_train, y_train, summery=True, workers=6)


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
    logger.info(f'True answers count {sum(mask)}')


if __name__ == '__main__':
    app()
