import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pickle
import numpy as np
from collections import defaultdict
from tensorflow.python.keras import Sequential, layers, losses
from tensorflow.python.keras.models import load_model
from keras.utils.np_utils import to_categorical

from ..logger import logger


class DocumentClasificator:
    model_path = os.path.dirname(__file__)
    word_index = []

    def __init__(self, model_name: str = 'model_1',
                 optimizer: str = 'adam', loss: str = losses.CategoricalCrossentropy(),
                 metric: str = 'accuracy'):
        self.optimizer = optimizer
        self.loss = loss
        self.metric = metric
        self.model_name = model_name
        self.model = Sequential()

    def load(self, summery=False):
        """Load model"""
        self.model = load_model(os.path.join(self.model_path, self.model_name))
        with open(os.path.join(self.model_path, self.model_name, 'word_index.pickle'), 'rb') as file:
            self.word_index = pickle.load(file)
        if summery:
            self.model.summary()

    def save(self):
        """Save model"""
        self.model.save(os.path.join(self.model_path, self.model_name))
        with open(os.path.join(self.model_path, self.model_name, 'word_index.pickle'), 'wb') as file:
            pickle.dump(self.word_index, file)

    @staticmethod
    def _get_layers(input_shape, output_shape, output_activation='softmax'):
        return [
            layers.Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=input_shape),
            layers.MaxPooling2D(),
            layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(output_shape, name='Output',activation=output_activation)
        ]

    def refacrtor_y_train(self, y_train):
        _word_index = defaultdict(list)
        for i, y in enumerate(y_train):
            _word_index[y].append(i)
        _word_index = sorted(_word_index.keys(), key=lambda k: k)
        self.word_index = list(_word_index)
        return to_categorical(np.array([self.word_index.index(value) for value in y_train]), len(self.word_index))

    def train(self, x_train: np.array, y_train: np.array, batch_size: int = 1, epochs: int = 3,
              validation_split: float = 0.2, *, save: bool = True, summery=False, workers=1, use_multiprocessing=True):
        """Train model and save"""
        logger.bigtext('Train Network')
        logger.info(f'Input - {x_train.shape}, Output - {y_train.shape}')
        input_shape = x_train[0].shape
        output_shape = len(set(y_train))
        y_train = self.refacrtor_y_train(y_train)

        self.model = Sequential(self._get_layers(input_shape, output_shape, 'softmax'), name=self.model_name)

        if summery:
            self.model.summary()
        self.model.compile(
            optimizer='rmsprop',
            loss=self.loss,
            metrics=[self.metric],
        )
        history = self.model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                                 validation_split=validation_split, use_multiprocessing=use_multiprocessing,
                                 workers=workers)
        if save:
            self.save()
        return history

    def evaluate(self, x: np.array, y: np.array, batch_size: int = 1,
                 save: bool = True):
        """Evaluate model and save"""
        history = self.model.evaluate(x, y, batch_size)
        if save:
            self.save()
        return history

    def predict(self, x: np.array):
        """Predict and return letter"""
        x = np.expand_dims(x, axis=0)
        y = self.model.predict(x)[0]
        index = np.argmax(y, 0)
        return index

    def predicts(self, x_list: np.array):
        """Predict and return list of letter"""
        y = self.model.predict(x_list)
        indexs = np.argmax(y, 1)
        return indexs
