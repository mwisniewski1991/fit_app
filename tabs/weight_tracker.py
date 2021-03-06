from dash import dcc, html
import plotly.graph_objects as go
import data_manager

colors = {
        'grid_color': 'rgba(0, 0, 0, 0.25)',
        'transparent': 'rgba(0, 0, 0, 0)',
        'white': 'rgb(255,255,255)',
    }

weight_layout = {
        'title': {'text': 'Weight tracker', 'color': colors['white'], 'font': {'size':27} }, 
        'font': {'family':'Georama', 'color': colors['white']},
        'paper_bgcolor': colors['transparent'],
        'plot_bgcolor': colors['transparent'],
        'xaxis': {'showline':False, 'gridcolor': colors['grid_color'], 'tickfont':{'size': 20}, 'tickformat': '%d.%m', 'ticklabelmode': 'period'},
        'yaxis': {'showline':True, 'gridcolor': colors['grid_color'], 'tickfont':{'size': 20}, 'dtick':0.5},
        'margin_b': 10, 'margin_t': 50, 'margin_r': 10,
        'margin': {'b': 40, 't': 50, 'r': 50, 'l': 60},
        'legend': {'title': {'text':'Day time'}, 'font': {'size':14} },
    }


def weight_tracker_frame():

    weight_df = data_manager.import_data()

    colors = {
        'grid_color': 'rgba(0, 0, 0, 0.25)',
        'transparent': 'rgba(0, 0, 0, 0)',
        'white': 'rgb(255,255,255)',
    }

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


    wt = html.Div(className='weightTracker', children=[
            html.Div(className='weightTracker__inputs', children=[
                html.Span(className='weightTracker__text', children='Put your current weight.'),
                dcc.Input(id='weight_input',
                    className='weightTracker__input',
                    type='number',
                    value=80.2,
                    step=0.1,
                ),
                html.Div(className='weightTracker__buttoncontainer', children=[
                    html.Button(id='weight_button_add',className='weightTracker__button', children='Submit'),
                    html.Button(id='weight_button_remove',className='weightTracker__button weightTracker__button--removed', children='Removed last'),
                ]),
                
            ]),

            html.Div(className='weightTracker__charts', children=[
                dcc.Graph(id='weight_chart',
                    figure={'data':[weight_trace_morning, weight_trace_evening], 'layout': weight_layout }, 
                    config={'displayModeBar': True},
                    # config={'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                    )
            ])
        ])

    return wt

if __name__ == '__main__':
    print(weight_tracker_frame())
