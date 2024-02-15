import os
import logging
from argparse import ArgumentParser

import psycopg2
import psycopg2.extensions


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cursor():
    logger.info("Создаём подключение к Postgres")
    params = {
        "host": os.environ['POSTGRES_HOST'],
        "port": os.environ['POSTGRES_PORT'],
        "user": os.environ['POSTGRES_USER'],
        "password": os.environ['POSTGRES_PASSWORD'],
    }
    conn = psycopg2.connect(**params)

    # дополнительные настройки
    psycopg2.extensions.register_type(
        psycopg2.extensions.UNICODE,
        conn
    )
    conn.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )
    cursor = conn.cursor()
    logger.info(f"Подключено: {cursor}")
    return conn, cursor


def fill_table(cursor, schema, table):
    """Пример команды
        \copy movie.ratings FROM '/usr/share/data_store/raw_data/ratings.csv' DELIMITER ',' CSV HEADER
    """
    data_exists_query = f"SELECT COUNT(*) FROM {schema}.{table}"
    cursor.execute(data_exists_query)

    data_exists_in_table = cursor.fetchall()[0][0] > 0

    if data_exists_in_table:
        truncate_table_query = f"TRUNCATE TABLE {schema}.{table}"
        cursor.execute(truncate_table_query)

    with open(f'/usr/share/data_store/raw_data/{table}.csv', 'r') as f:
        sql = f"COPY {schema}.{table} FROM STDIN DELIMITER ',' CSV HEADER"
        logger.info(f'Загружаем {schema}.{table} ...')
        cursor.copy_expert(sql, f)


def user_exist(psql_cursor, username):
    sql_str = f"SELECT 1 FROM pg_roles WHERE rolname='{username}'"
    check_user = False
    psql_cursor.execute(sql_str)
    if psql_cursor.rowcount > 0:
        check_user = True
    return check_user


def create_postgres_user(psql_cursor, username, userpass, is_superuser=False):
    if user_exist(psql_cursor, username):
        logger.info('Пользователь %s существует', username)
    else:
        psql_cursor.execute(f'CREATE DATABASE {username}')
        psql_cursor.execute(f"create user {username} with encrypted password '{userpass}'")
        psql_cursor.execute(f"""GRANT ALL PRIVILEGES ON DATABASE {username} TO {username}""")
        if is_superuser:
            psql_cursor.execute(f"ALTER USER {username} WITH SUPERUSER")


def table_row_count(psql_cursor, table_name):
    sql_str = f"SELECT COUNT(*) as cnt FROM movie.{table_name}"
    logger.info('Проверяем количество строк в таблице...')
    psql_cursor.execute(sql_str)
    row_count = int(tuple(i[0] for i in cursor.fetchall())[0])
    logger.info('Таблица %s содержит %s строк', table_name, row_count)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-s', '--scenario', dest='scenario', required=True, help='Сценарий: extract, transform')
    args = parser.parse_args()
    conn, cursor = get_cursor()
    tables = ('links', 'ratings', 'events')
    if args.scenario == 'load':
        for tbl_name in tables:
            fill_table(cursor, 'movie', tbl_name)
        logger.info('Tables created')
        create_postgres_user(
            cursor,
            username='metabase',
            userpass=os.environ['METABASE_PASS'],
            is_superuser=True
        )
    elif args.scenario == 'row_count':
        table_row_count(cursor, 'ratings')
    conn.commit()
