from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import requests

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(
    style={'backgroundColor': 'black'},
    children=[
        html.H1(
            "MF 3.2 - Cartas de Controle",
            style={
                'color': 'white',
                'textAlign': 'center',
                'fontSize': '36px',
                'marginBottom': '20px',
                'fontWeight': 'bold',
                'textShadow': '2px 2px #ff0000',
            }
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(id="ait01_indicator"), width=6),
            dbc.Col(dcc.Graph(id="ait02_indicator"), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="tit01_indicator"), width=6),
            dbc.Col(dcc.Graph(id="tit02_indicator"), width=6),
        ]),
        dcc.Interval(id="interval", interval=10000),
    ]
)

@app.callback(
    Output("ait01_indicator", "figure"),
    Output("ait02_indicator", "figure"),
    Output("tit01_indicator", "figure"),
    Output("tit02_indicator", "figure"),
    Input("interval", "n_intervals"),
)
def update_figure(n_intervals):
    def get_data(tag):
        one_hour_later = datetime.now() - timedelta(hours=1)
        start_time = one_hour_later.strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        url = "http://bbathena.amyris.local/historian/api"
        params = {"tag": tag, "start": start_time, "end": end_time, "samples": "1m"}
        data = requests.get(url, params=params).json()["DADOS"]
        df = pd.DataFrame(data)
        df.Timestamp = pd.to_datetime(df.Timestamp)
        return df

    def create_indicator(data, y_label, line_y):
        one_hour_later = datetime.now() - timedelta(hours=1)
        fig = px.line(x=data.Timestamp, y=data.Value, height=300, template="plotly_dark")
        fig.update_layout(
            xaxis=dict(title="Data e Hora"),
            yaxis=dict(title=y_label),
            transition_duration=500
        )
        fig.add_shape(
            dict(
                type="line",
                x0=one_hour_later,
                x1=datetime.now(),
                y0=line_y[0],
                y1=line_y[0],
                line=dict(color="Red", width=2)
            )
        )
        fig.add_shape(
            dict(
                type="line",
                x0=one_hour_later,
                x1=datetime.now(),
                y0=line_y[1],
                y1=line_y[1],
                line=dict(color="Red", width=2)
            )
        )
        return fig

    data_ait01 = get_data("BB04632AIT001")
    data_ait02 = get_data("BB04632AIT002")
    data_tit01 = get_data("BB04632TIT001")
    data_tit02 = get_data("BB04632TIT002")

    ait01_indicator = create_indicator(data_ait01, "pH", [6, 5])
    ait02_indicator = create_indicator(data_ait02, "pH", [6, 5])
    tit01_indicator = create_indicator(data_tit01, "TIT01", [28, 31])
    tit02_indicator = create_indicator(data_tit02, "TIT02", [28, 31])

    return ait01_indicator, ait02_indicator, tit01_indicator, tit02_indicator

if __name__ == "__main__":
    app.run_server(debug=True)
