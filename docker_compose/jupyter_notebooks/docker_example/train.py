import pickle
import os
import logging
from pathlib import Path

import numpy as np
from sklearn.tree import DecisionTreeClassifier

logging.basicConfig(filename="/www/classifier/data/service.log", level=logging.INFO)

# загрузка данных
data_source = np.genfromtxt('data/client_segmentation.csv', delimiter=',', skip_header=1)
X = data_source[:, :3]
y = data_source[:, 3]
# обучение модели
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X, y)
# сохраняем модель внутри контейнера в директории /www/classifier
with open('clf.pkl', 'wb') as f:
    pickle.dump(clf, f)
    logging.info('Модель обучена и сохранена в %s' % Path().absolute())
print("Модель обучена!")
