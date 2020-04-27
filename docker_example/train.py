import pickle
import os
import logging
from pathlib import Path

import numpy as np
from sklearn.tree import DecisionTreeClassifier

LOG_FORMAT = '%(asctime)s | %(levelname)-8s | %(filename)-25.25s:%(lineno)-4d | %(message)s'
log_filename = "/www/classifier/data/service.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format=LOG_FORMAT)

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
with open('data/clf.pkl', 'wb') as f:
    pickle.dump(clf, f)
print(f"Модель обучена! Лог: {log_filename}")
