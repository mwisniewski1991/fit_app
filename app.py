from dash import dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from tabs.weight_tracker import weight_tracker_frame, colors, weight_layout
import data_manager

app = dash.Dash(__name__)
app.title = 'FitApp'
app.layout = html.Div(children=[
    dcc.Store(id='local_store', storage_type='local'),
    html.Header(className='header', children=[
        html.H1(className='header__title', children='Fit App')
    ]),
    html.Main(className='main', children=[
        weight_tracker_frame(),
    ])
])

@app.callback(
    [
    Output(component_id='weight_chart', component_property='figure'),
    Output(component_id='weight_button_add', component_property='n_clicks'),
    Output(component_id='weight_button_remove', component_property='n_clicks'),
    Output(component_id='local_store', component_property='data')
    ],
    [
    Input(component_id='weight_button_add', component_property='n_clicks'),
    Input(component_id='weight_button_remove', component_property='n_clicks'),
    ],
    [State(component_id='weight_input', component_property='value'),
    State(component_id='local_store', component_property='data')
    ]
)
def add_new_weight_data(n_clicks_add, n_clicks_remove, weight, store_data):

    # if n_clicks_add is None and n_clicks_remove is None: 
    #     raise PreventUpdate
    new_data = {}
    if n_clicks_remove == 1:
        if store_data:
            data_manager.remove_last_register(store_data['report_time'])
        new_data = {}

    if n_clicks_add == 1:
        new_data = data_manager.add_new_data(weight)

    weight_df = data_manager.import_data()
    
    q_morning = weight_df['part_of_day'] == 'morning'
    q_evening = weight_df['part_of_day'] == 'evening'
    
    weight_trace_morning = go.Scatter(
        x=weight_df[q_morning]['report_time'],
        y=weight_df[q_morning]['weight'],
        line_color='yellow')

    weight_trace_evening = go.Scatter(
        x=weight_df[q_evening]['report_time'],
        y=weight_df[q_evening]['weight'],
        line_color='blue')

    return {'data': [weight_trace_morning, weight_trace_evening], 'layout': weight_layout}, None, None, new_data

if __name__ == '__main__':
    app.run_server(debug=True)