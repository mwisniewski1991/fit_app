from dash import dash, dcc, html, Input, Output
import plotly.graph_objects as go
from tabs.weight_tracker import weight_tracker_frame

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Header(className='header', children=[
        html.H1(className='header__title', children='Fit App')
    ]),
    html.Main(className='main', children=[
        weight_tracker_frame(),

    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)