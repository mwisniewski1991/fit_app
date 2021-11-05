from dash import dcc, html
import plotly.graph_objects as go
import data_manager

colors = {
        'grid_color': 'rgba(0, 0, 0, 0.25)',
        'transparent': 'rgba(0, 0, 0, 0)',
        'white': 'rgb(255,255,255)',
    }

weight_layout = {
        'title': {'text': 'Weight tracker', 'color': colors['white']}, 
        'font': {'family':'Georama', 'color': colors['white']},
        'paper_bgcolor': colors['transparent'],
        'plot_bgcolor': colors['transparent'],
        'xaxis': {'showline':False, 'gridcolor': colors['grid_color'], 'tickformat': '%Y-%m-%d', 'ticklabelmode': 'period'},
        'yaxis': {'showline':True, 'gridcolor': colors['grid_color']},
        'margin_b': 10, 'margin_t': 50, 'margin_r': 10,
        'margin': {'b': 40, 't': 50, 'r': 50, 'l': 40},
        'showlegend': False,
    }

def weight_tracker_frame():

    weight_df = data_manager.import_data()

    colors = {
        'grid_color': 'rgba(0, 0, 0, 0.25)',
        'transparent': 'rgba(0, 0, 0, 0)',
        'white': 'rgb(255,255,255)',
    }

    weight_layout = {
            'title': {'text': 'Weight tracker', 'color': colors['white']}, 
            'font': {'family':'Georama', 'color': colors['white']},
            'paper_bgcolor': colors['transparent'],
            'plot_bgcolor': colors['transparent'],
            'xaxis': {'showline':False, 'gridcolor': colors['grid_color'], 'tickformat': '%Y-%m-%d', 'ticklabelmode': 'period'},
            'yaxis': {'showline':True, 'gridcolor': colors['grid_color']},
            'margin_b': 10, 'margin_t': 50, 'margin_r': 10,
            'margin': {'b': 40, 't': 50, 'r': 50, 'l': 40},
            'showlegend': False,
        }

    weight_trace = go.Scatter(
        x=weight_df['report_time'],
        y=weight_df['weight'],
        line_color=colors['white'])

    wt = html.Div(className='weightTracker', children=[
            html.Div(className='weightTracker_inputs', children=[
                html.Span(className='inputs__text', children='Put your current weight.'),
                dcc.Input(id='weight_input',
                    className='inputs__input',
                    type='number',
                    value=80.2,
                    step=0.1,
                ),
                html.Div(className='inputs__buttonConteiner', children=[
                    html.Button(id='weight_button_add',className='inputs__button', children='Submit'),
                    html.Button(id='weight_button_remove',className='inputs__button inputs__button--removed', children='Removed last'),
                ]),
                
            ]),

            html.Div(className='charts', children=[
                dcc.Graph(id='weight_chart',
                    figure={'data':[weight_trace], 'layout': weight_layout }, 
                    config={'displayModeBar': True},
                    # config={'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                    )
            ])
        ])

    return wt

if __name__ == '__main__':
    print(weight_tracker_frame())
