import os
import psycopg2
import psycopg2.extensions
import logging


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
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )
    cursor = conn.cursor()
    logger.info(f"Подключено: {cursor}")
    return conn, cursor


def get_table_columns(schema, table):
    get_table_columns_query = f"""
    SELECT column_name
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}';
    """
    cursor.execute(get_table_columns_query)
    return [c[0] for c in cursor.fetchall()]


def fill_table(schema, table):
    columns = get_table_columns(schema, table)
    columns_without_id = [c for c in columns if c != 'id']

    with open(f'/usr/share/data_store/raw_data/{table}.csv', 'r') as f:
        sql = f"""
        COPY {schema}.{table} ({', '.join(columns_without_id)})
        FROM STDIN DELIMITER ',' CSV HEADER
        """
        cursor.copy_expert(sql, f)
        logger.info(f'загружаем {schema}.{table}')

    row_columns = lambda name: ', '.join(
        f'{name}.{column}'
        for column in columns_without_id
    )

    # NOTE: idk why this statement do not touch some rows, but it delete mostly duplicates
    # Delete dupliacates
    delete_duplicates_query = f"""
    DELETE FROM {schema}.{table} a
    USING {schema}.{table} b
    WHERE a.id < b.id AND ROW({row_columns('a')}) = ROW({row_columns('b')});
    """
    cursor.execute(delete_duplicates_query)


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


if __name__=='__main__':
    conn, cursor = get_cursor()
    fill_table('movie', 'links')
    fill_table('movie', 'ratings')
    fill_table('movie', 'events')
    create_user(cursor, username='mai', userpass='1930')
    conn.commit()
