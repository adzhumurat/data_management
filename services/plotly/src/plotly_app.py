import os

import pandas as pd
from sqlalchemy import create_engine
# from dash import *
import plotly.express as px
from dash import Dash, html, dcc, Output, Input
from dash_core_components import Interval


db_params = {
    "host": os.environ['POSTGRES_HOST'],
    "port": os.environ['POSTGRES_PORT'],
    "user": os.environ['POSTGRES_USER'],
    "password": os.environ['POSTGRES_PASSWORD']
}
# db_params.update({"host": "64.226.98.30"})

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

df = pd.read_sql(sql_str, con=engine)
df['dt'] = pd.to_datetime(df['dt'])

app = Dash(__name__)
server = app.server

fig = px.bar(df, x='dt', y='uniq_users',
             labels={'num_users': 'Uniq Users', 'hour': 'Hour'},
             title='Number of Users per Hour')


app.layout = html.Div(children=[
    html.H1(children='EventAlly analytics'),

    html.Div(children='''
        Tg bot uniq users by hour
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

        # Interval component to trigger updates every 5 minutes
    Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('example-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    global df

    df = pd.read_sql(sql_str, con=engine)
    df['dt'] = pd.to_datetime(df['dt'])

    updated_fig = px.bar(df, x='dt', y='uniq_users',
                         labels={'num_users': 'Number of Users', 'hour': 'Hour'},
                         title='Number of Users per Hour')

    return updated_fig

if __name__ == '__main__':
    app.run_server(port=8002, debug=True)
