from dash import dcc, html
import plotly.graph_objects as go
import tabs.data as datamw

def weight_tracker_frame():

    weight_df = datamw.import_data()

    colors = {
        'grid_color': 'rgba(0, 0, 0, 0.25)',
        'transparent': 'rgba(0, 0, 0, 0)',
        'white': 'rgb(255,255,255)',
    }
    
    weight_trace = go.Scatter(
        x=weight_df['report_date'],
        y=weight_df['weight'],
        line_color=colors['white'])

    layout = {
        'title': {'text': 'Weight tracker', 'color': colors['white']}, 
        'font': {'family':'Georama', 'color': colors['white']},
        'paper_bgcolor': colors['transparent'],
        'plot_bgcolor': colors['transparent'],
        'xaxis': {'showline':False, 'gridcolor': colors['grid_color']},
        'yaxis': {'showline':True, 'gridcolor': colors['grid_color']},
        'margin_b': 10, 'margin_t': 50, 'margin_r': 10,
        'margin': {'b': 40, 't': 50, 'r': 50, 'l': 20},
        'showlegend': False,
    }


    wt = html.Div(className='weightTracker', children=[
            html.Div(className='inputs', children=[
                html.Span(className='inputs__text', children='Put your current weight.'),
                dcc.Input(
                className='inputs__input',
                type='number',
                value=80.2,
                step=0.1,
                ),
                html.Button(className='inputs__button', children='Submit')
            ]),

            html.Div(className='charts', children=[
            dcc.Graph(figure={'data':[weight_trace], 'layout':layout }, 
                # config={'displayModeBar': False},
                config={'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                )
            ])
        ])
    return wt



if __name__ == '__main__':
    print(weight_tracker_frame())
