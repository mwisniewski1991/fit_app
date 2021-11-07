from dash import dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from tabs.weight_tracker import weight_tracker_frame, colors, weight_layout
import data_manager

app = dash.Dash(__name__)
app.title = 'FitApp'
app.layout = html.Div(children=[
    html.Header(className='header', children=[
        html.H1(className='header__title', children='Fit App')
    ]),
    html.Main(className='main', children=[
        weight_tracker_frame(),

    ])
])
# Input(component_id='weight_input', component_property='value')
@app.callback(
    [
    Output(component_id='weight_chart', component_property='figure'),
    Output(component_id='weight_button_add', component_property='n_clicks'),
    Output(component_id='weight_button_remove', component_property='n_clicks'),
    ],
    [
    Input(component_id='weight_button_add', component_property='n_clicks'),
    Input(component_id='weight_button_remove', component_property='n_clicks'),
    ],
    State(component_id='weight_input', component_property='value')
)
def add_new_weight_data(n_clicks_add, n_clicks_remove, weight):
    print('-------------')
    print(f'{n_clicks_add=}')
    print(f'{n_clicks_remove=}')

    if n_clicks_add is None and n_clicks_remove is None: 
        print('Prevent update')
        raise PreventUpdate

    elif n_clicks_remove == 1:
        print('REMOVED')

    elif n_clicks_add == 1:
        print('UPDATE')
        data_manager.add_new_data(weight)

    weight_df = data_manager.import_data()
    weight_trace = go.Scatter(
        x=weight_df['report_time'],
        y=weight_df['weight'],
        line_color=colors['white'])

    return {'data': [weight_trace], 'layout': weight_layout}, None, None

# @app.callback(
#     Output(component_id='weight_chart', component_property='figure'),
#     Input(component_id='weight_button_add', component_property='n_clicks'),
# )
# def removed_weight_data(n_clicks):
#     print(n_clicks)
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         data_manager.add_new_data(weight)
#         weight_df = data_manager.import_data()
#         weight_trace = go.Scatter(
#             x=weight_df['report_time'],
#             y=weight_df['weight'],
#             line_color=colors['white']
#         )

#         return {'data': [weight_trace], 'layout': weight_layout}


if __name__ == '__main__':
    app.run_server(debug=True)