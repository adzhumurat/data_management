"""
Умеет выполнять классификацию клиентов по трём фичам

Запускаем из python3:
    python3 service.py
Проверяем работоспособность:
    curl http://127.0.0.1:5000/
"""
import http.server
import json
import os
import socketserver
from http import HTTPStatus
import logging
import psycopg2

# файл, куда посыпятся логи модели
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename="/www/app/service.log", level=logging.INFO, format=FORMAT)


class Handler(http.server.SimpleHTTPRequestHandler):
    """Простой http-сервер"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_response(self) -> dict:
        response = {'health-check': 'ok'}
        params_parsed = self.path.split('?')
        if self.path.startswith('/ping/'):
            response = {'message': 'pong'}
        # Реализуем API profile
        elif self.path.startswith('/user/profile'):
            user_id = self.path.split('/')[-1]
            user_profile = [None, None]
            logging.info(f'Поступил запрос по пользователю {user_id}')
            try:
                user_profile = postgres_interactor.get_sql_result(f"""
                    SELECT 
                        COUNT(rating) as rate_count,
                        AVG(rating) as avg_rating
                    FROM ratings
                    WHERE
                        userId = {user_id}
                """)[0]
            except Exception as e:
                logging.info(f'Произошла ошибка запроса:\n{e}')
            response = {'user_id': user_id, 'num_rating': user_profile[0], 'avg_rating': user_profile[1]}
        # Реализуем API /user/watchhistory/user_id
        elif self.path.startswith('/user/watchhistory'):
            """ВАШ КОД ТУТ
            
            Для каждого переданного user_id API должен возвращать историю оценок, которые ставил этот user_id в виде

            [
                {"movie_id": 4119470, "rating": 4, "timestamp": "2019-09-03 10:00:00"},
                {"movie_id": 5691170, "rating": 2, "timestamp": "2019-09-05 13:23:00"},
                {"movie_id": 3341191, "rating": 5, "timestamp": "2019-09-08 16:40:00"}
            ]
            """

        return response

    def do_GET(self):
        # заголовки ответа
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(self.get_response()).encode())


class PostgresStorage:
    def __init__(self):
        # подключение к Postgres
        params = {
            "host": os.environ['APP_POSTGRES_HOST'],
            "port": os.environ['APP_POSTGRES_PORT'],
            "user": 'postgres'
        }
        self.conn = psycopg2.connect(**params)

        # дополнительные настройки
        psycopg2.extensions.register_type(
            psycopg2.extensions.UNICODE,
            self.conn
        )
        self.conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )
        self.cursor = self.conn.cursor()

    def get_sql_result(self, sql_str):
        """Исполняем SQL и возвращаем PandasDF"""
        # исполняем SQL
        self.cursor.execute(sql_str)
        # получаем результат запроса
        query_data = [a for a in self.cursor.fetchall()]
        # коммит необязательно, но для порядка необходим
        self.conn.commit()
        return query_data


postgres_interactor = PostgresStorage()
logging.info('Инициализирован класс для работы с Postgres')

if __name__ == '__main__':
    classifier_service = socketserver.TCPServer(('', 5000), Handler)
    logging.info('Приложение инициализировано')
    classifier_service.serve_forever()
