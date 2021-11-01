from dash import dash, dcc, html, Input, Output
import plotly.graph_objects as go
from tabs.weight_tracker import weight_tracker_frame, colors, weight_layout
import data_manager


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Header(className='header', children=[
        html.H1(className='header__title', children='Fit App')
    ]),
    html.Main(className='main', children=[
        weight_tracker_frame(),

    ])
])

@app.callback(
    Output(component_id='weight_chart', component_property='figure'),
    [   Input(component_id='weight_input', component_property='value'),
        Input(component_id='weight_button', component_property='n_clicks')
    ]
)
def add_new_weight_data(weight, n_clicks):

    if n_clicks != None:
        print('DATA TO DB')
        print(weight, n_clicks)
    else:
        print('ONLY LOAD')
        print(weight)

    weight_df = data_manager.import_data()
    weight_trace = go.Scatter(
        x=weight_df['report_time'],
        y=weight_df['weight'],
        line_color=colors['white']
    )

    return {'data': [weight_trace], 'layout': weight_layout}

if __name__ == '__main__':
    app.run_server(debug=True)