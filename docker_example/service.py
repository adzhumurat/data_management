"""
Умеет выполнять классификацию клиентов по трём фичам

Запускаем из python3:
    python3 service.py
Проверяем работоспособность:
    curl http://127.0.0.1:5000/
"""
import numpy as np
import http.server
import json
import os
import pickle
import socketserver
import sys
from http import HTTPStatus
from re import compile
import logging
from sklearn.tree import DecisionTreeClassifier

# файл, куда посыпятся логи модели
logging.basicConfig(filename="/www/classifier/data/service.log", level=logging.INFO)


def parse_params(params) -> dict:
    """
        Выдираем параметры из GET-запроса
    """
    params_list = params.split('&')
    params_dict = {'x1': None, 'x2': None, 'x3': None}
    for param in params_list:
        key, value = param.split('=')
        params_dict[key] = float(value)
    return params_dict


class Handler(http.server.SimpleHTTPRequestHandler):
    """Простой http-сервер"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_response(self) -> dict:
        response = {'ping': 'ok'}
        params_parsed = self.path.split('?')
        if len(params_parsed) == 2 and self.path.startswith('/classifier'):
            params = params_parsed[1]
            params_dict = parse_params(params)
            response = params_dict
            user_features = np.array([params_dict['x1'], params_dict['x2'], params_dict['x3']]).reshape(1, -1)
            predicted_class = int(classifier_model.predict(user_features)[0])
            logging.info('predicted_class %s' % predicted_class)
            response.update({'predicted_class': predicted_class})
        elif self.path.startswith('/ping/'):
            response = {'message': 'pong'}

        return response

    def do_GET(self):
        # заголовки ответа
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.get_response()).encode())


logging.info('Загружаем обученную модель')
with open('/www/classifier/clf.pkl', 'rb') as f:
    classifier_model = pickle.load(f)
    logging.info('Модель загружена: %s' % classifier_model)

if __name__ == '__main__':
    classifier_service = socketserver.TCPServer(('', 5000), Handler)
    classifier_service.serve_forever()
