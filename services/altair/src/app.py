import time
import os
import threading

from sqlalchemy import create_engine
import psycopg2
import streamlit as st
import pandas as pd
import altair as alt

db_params = {
    "host": os.environ['POSTGRES_HOST'],
    "port": os.environ['POSTGRES_PORT'],
    "user": os.environ['POSTGRES_USER'],
    "password": os.environ['POSTGRES_PASSWORD']
}


engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}")
print('Connected to postgres')

sql_str = """
SELECT
    to_char(to_timestamp(timestamp), 'YYYY/MM/DD') as dt,
    COUNT(DISTINCT userId) as uniq_users
FROM movie.ratings
WHERE
    to_char(to_timestamp(timestamp), 'YYYY/MM/DD') BETWEEN '2015/07/01' AND '2015/12/31'
GROUP BY 1
ORDER BY 1 DESC
"""

def load_data():
    df = pd.read_sql(sql_str, engine)
    return df

def reload_data_periodically():
    while True:
        # Reload data every 5 minutes (adjust as needed)
        time.sleep(300)
        st.cache_data.clear()
        load_data


def main():
    app_formal_name = "Live streamplit analytics"
    st.set_page_config(
        layout="wide", page_title=app_formal_name,
    )
    st.sidebar.title("Data overview")

    df = st.cache_data(load_data)()

    st.sidebar.write("num points: %d" % len(df))

    title_element = st.empty()
    title_element.title("awesome analytics")

    chart = alt.Chart(df).mark_line().encode(
        x='dt',
        y='uniq_users',
        tooltip=['dt', 'uniq_users']
    ).properties(
        width=600,
        height=300
    ).interactive()
    st.altair_chart(chart, use_container_width=True)


if __name__ == '__main__':
    threading.Thread(target=reload_data_periodically, daemon=True).start()
    main()
