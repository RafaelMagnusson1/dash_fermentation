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
    dcc.Graph(id="ph_indicator"),

    dcc.Interval(id="interval", interval = 10000),
    
    ])

@app.callback(
        Output("ph_indicator","figure"),
        Input("interval","n_intervals"),
)
def update_figure(n_intervals):

    one_hour_later = datetime.now() - timedelta(hours=1)
    start_time = one_hour_later.strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    url = "http://bbathena.amyris.local/historian/api"
    params = {"tag":"BB04632AIT002","start":start_time,"end":end_time, "samples":"1m"}

    data = requests.get(url, params=params).json()["DADOS"]
    data = pd.DataFrame(data)

    data.Timestamp = pd.to_datetime(data.Timestamp)

    ph_indicator = px.line(x=data.Timestamp, y=data.Value, height=300, template="plotly_dark")
    ph_indicator.update_layout(
        xaxis=dict(title="Data e Hora"),
        yaxis=dict(title="pH"),
        transition_duration=500
    )

    ph_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=6,
            y1=6,
            line=dict(color="Red", width=2)
        )
    )

    ph_indicator.add_shape(
        dict(
            type="line",
            x0=one_hour_later,
            x1=datetime.now(),
            y0=5,
            y1=5,
            line=dict(color="Red", width=2)
        )
    )

    return ph_indicator

if __name__ == "__main__":
    app.run_server(debug=True)