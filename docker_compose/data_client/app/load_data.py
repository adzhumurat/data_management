import os
import psycopg2
import psycopg2.extensions
import logging
import sys


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cursor():
    logger.info("Создаём подключение к Postgres")
    params = {
        "host": os.environ['APP_POSTGRES_HOST'],
        "port": os.environ['APP_POSTGRES_PORT'],
        "user": 'postgres'
    }
    conn = psycopg2.connect(**params)

    # дополнительные настройки
    psycopg2.extensions.register_type(
        psycopg2.extensions.UNICODE,
        conn
    )
    conn.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED
    )
    cursor = conn.cursor()
    logger.info(f"Подключено: {cursor}")
    return conn, cursor


def fill_table(schema, table, truncate):
    if truncate:
        logger.info(f"Очистка {schema}.{table}")
        truncate_sql = f"TRUNCATE TABLE {schema}.{table}"
        cursor.execute(truncate_sql)
        logger.info(f"{schema}.{table} очищена")
    with open(f'/usr/share/data_store/raw_data/{table}.csv', 'r') as f:
        sql = f"COPY {schema}.{table} FROM STDIN DELIMITER ',' CSV HEADER"
        cursor.copy_expert(sql, f)
        logger.info(f'загружаем {schema}.{table}')

def user_exist(psql_cursor, username):
    sql_str = f"SELECT 1 FROM pg_roles WHERE rolname='{username}'"
    check_user = False
    psql_cursor.execute(sql_str)
    if cursor.rowcount > 0:
        check_user = True
    return check_user


def create_user(psql_cursor, username, userpass):
    if user_exist(psql_cursor, username):
        logger.info('Пользователь %s существует', username)
    else:
        cursor.execute(f"create user {username} with encrypted password '{userpass}'")
        cursor.execute(f"""
           GRANT CONNECT ON DATABASE postgres TO {username};
           GRANT USAGE ON SCHEMA movie TO {username};
           GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA movie TO {username};
           GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA movie TO {username};
           GRANT ALL PRIVILEGES ON TABLE movie.links TO {username};
           GRANT ALL PRIVILEGES ON TABLE movie.ratings TO {username};
        """)


if __name__ == '__main__':
    conn, cursor = get_cursor()
    truncate = False
    if len(sys.argv) > 1 and sys.argv[1] == '-r':
        truncate = True
    fill_table('movie', 'links', truncate)
    fill_table('movie', 'ratings', truncate)
    fill_table('movie', 'events', truncate)
    create_user(cursor, username='mai', userpass='1930')
    conn.commit()
