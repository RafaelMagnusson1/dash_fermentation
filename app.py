from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import requests
import json

app = Dash(__name__)

app.layout = html.Div([

    html.H1("MF 3.2"),    
    dcc.Graph(id="ait01_indicator"),
    dcc.Graph(id="ait02_indicator"),
    dcc.Graph(id="tit01_indicator"),
    dcc.Graph(id="tit02_indicator"),

    dcc.Interval(id="interval", interval = 10000),
    
    ])

@app.callback(
        Output("ait01_indicator","figure"),
        Output("ait02_indicator","figure"),
        Output("tit01_indicator","figure"),
        Output("tit02_indicator","figure"),
        Input("interval","n_intervals"),
)
def update_figure(n_intervals):

    one_hour_later = datetime.now() - timedelta(hours=1)
    start_time = one_hour_later.strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    url = "http://bbathena.amyris.local/historian/api"

    params_ait01 = {"tag":"BB04632AIT001","start":start_time,"end":end_time, "samples":"1m"}
    params_ait02 = {"tag":"BB04632AIT002","start":start_time,"end":end_time, "samples":"1m"}    
    params_tit01 = {"tag":"BB04632TIT001","start":start_time,"end":end_time, "samples":"1m"}
    params_tit02 = {"tag":"BB04632TIT002","start":start_time,"end":end_time, "samples":"1m"}


    data_ait01 = requests.get(url, params=params_ait01).json()["DADOS"]
    data_ait01 = pd.DataFrame(data_ait01)
    data_ait01.Timestamp = pd.to_datetime(data_ait01.Timestamp)


    data_ait02 = requests.get(url, params=params_ait02).json()["DADOS"]
    data_ait02 = pd.DataFrame(data_ait02)
    data_ait02.Timestamp = pd.to_datetime(data_ait02.Timestamp)

    data_tit01 = requests.get(url, params=params_tit01).json()["DADOS"]
    data_tit01 = pd.DataFrame(data_tit01)
    data_tit01.Timestamp = pd.to_datetime(data_tit01.Timestamp)


    data_tit02 = requests.get(url, params=params_tit02).json()["DADOS"]
    data_tit02 = pd.DataFrame(data_tit02)
    data_tit02.Timestamp = pd.to_datetime(data_tit02.Timestamp)

    ait01_indicator = px.line(x=data_ait01.Timestamp, y=data_ait01.Value, height=300, template="plotly_dark")

    ait01_indicator.update_layout(
        xaxis=dict(title="Data e Hora"),
        yaxis=dict(title="pH"),
        transition_duration=500
    )

    ait01_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=6,
            y1=6,
            line=dict(color="Red", width=2)
        )
    )

    ait01_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=5,
            y1=5,
            line=dict(color="Red", width=2)
        )
    )

    ait02_indicator = px.line(x=data_ait02.Timestamp, y=data_ait02.Value, height=300, template="plotly_dark")
    
    ait02_indicator.update_layout(
        xaxis=dict(title="Data e Hora"),
        yaxis=dict(title="pH"),
        transition_duration=500
    )

    ait02_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=6,
            y1=6,
            line=dict(color="Red", width=2)
        )
    )

    ait02_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=5,
            y1=5,
            line=dict(color="Red", width=2)
        )
    )

    tit01_indicator = px.line(x=data_tit01.Timestamp, y=data_tit01.Value, height=300, template="plotly_dark")

    tit01_indicator.update_layout(
        xaxis=dict(title="Data e Hora"),
        yaxis=dict(title="TIT01"),
        transition_duration=500
    )

    tit01_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=28,
            y1=28,
            line=dict(color="Red", width=2)
        )
    )

    tit01_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=31,
            y1=31,
            line=dict(color="Red", width=2)
        )
    )

    tit02_indicator = px.line(x=data_tit02.Timestamp, y=data_tit02.Value, height=300, template="plotly_dark")
    
    tit02_indicator.update_layout(
        xaxis=dict(title="Data e Hora"),
        yaxis=dict(title="TIT02"),
        transition_duration=500
    )

    tit02_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=28,
            y1=28,
            line=dict(color="Red", width=2)
        )
    )

    tit02_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=31,
            y1=31,
            line=dict(color="Red", width=2)
        )
    )
    return ait01_indicator, ait02_indicator, tit01_indicator, tit02_indicator

if __name__ == "__main__":
    app.run_server(debug=True)