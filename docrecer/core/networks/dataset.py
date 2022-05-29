import os
import cv2
import numpy as np
from sklearn.utils import shuffle
from collections import defaultdict
from itertools import cycle


def load_dataset(path):
    x_train, y_train = [], []
    files = defaultdict(list)
    for in_path, _, file in os.walk(path):
        folder_name = os.path.split(in_path)[-1]
        for f in file:
            file_path = os.path.join(in_path, f)
            image = cv2.imread(file_path)
            image = cv2.resize(image, (240, 320))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            files[folder_name].append(image)
            for _ in range(3):
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
                image = cv2.resize(image, (240, 320))
                files[folder_name].append(image)
    max_len = len(list(files.values())[0])
    for key, value in files.items():
        if max_len < len(value):
            max_len = len(value)
    for key, values in files.items():
        _iter = cycle(values)
        for _ in range(max_len):
            image = next(_iter)
            x_train.append(image)
            y_train.append(key)
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_train, y_train = shuffle(x_train, y_train)
    x_train = np.expand_dims(x_train, 3)
    return x_train, y_train
