# Bar and Parallel graph in one row
import dash
import dash_core_components as dcc                                                                  # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  
import plotly.graph_objects as go

import plotly.figure_factory as ff
import numpy as np
import pandas as pd

df_sample = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/minoritymajority.csv')
df_sample_r = df_sample[df_sample['STNAME'] == 'California']
values = df_sample_r['TOT_POP'].tolist()
fips = df_sample_r['FIPS'].tolist()
colorscale = [
    'rgb(193, 193, 193)',
    'rgb(239,239,239)',
    'rgb(195, 196, 222)',
    'rgb(144,148,194)',
    'rgb(101,104,168)',
    'rgb(65, 53, 132)'
]
fig_map = ff.create_choropleth(
    fips=fips, values=values, scope=['CA', 'AZ', 'Nevada', 'Oregon', ' Idaho'],
    binning_endpoints=[14348, 63983, 134827, 426762, 2081313], colorscale=colorscale,
    county_outline={'color': 'rgb(255,255,255)', 'width': 0.5}, round_legend_values=True,
    legend_title='Population by County', title='California and Nearby States'
)




fig = go.Figure(data=
    go.Parcoords(
        line_color='blue',
        dimensions = list([
            dict(
                range = [1,5],              # range of the bar. if i dont have this, will be long (bad)
                tickvals = [1,2,4,5],
                label = 'Stuff',            # name of the bar 
                values = [2,4],         # marks on the bar
                ticktext = ['text 1', 'text 2', 'text 3', 'text 4']
            ),
            dict(                           # 1) dict() the first column and it has:
                label = 'A',                    # 2) Name of the bar
                tickvals = [1,2,4,5], 
                range = [1,5],                  # 3) the range of this bar. If i dont set it, bar will be long
                values = [1,4]                # 5) the values in that bar. each index is connected to the index of the next bar
            ),
            dict(
                label = 'B',
                range = [1,5],                
                tickvals = [1,2,4,5],  
                values = [3,1.5]
            ),
            dict(
                label = 'c', 
                tickvals = [1,2,4,5], 
                range = [1,5],
                values = [4,2]
            )
        ])
    )
)
# Bootstrap CSS:
external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']                              # external CSS file
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)                                # initialize app with the external CSS file
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(  
    html.Div(style={'backgroundColor': colors['background']}, children=[              # GLOBAL DIV                                                                
        html.Div([          # COMPONENT ROW 1 DIV
            html.H1(children='Hello Dash B',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
            }),                                                                                     # same as html.H1('Hello Dash')
            html.Div(children="Dash: A web application framework for Python.",
                style={
                    'textAlign': 'center',
                    'color': colors['text']
            }),
        ], className = "row"),

        html.Div([          # 2 GRAPHS IN ROW 2 DIV
            html.Div([          # INDIVIDUAL GRAPH COLUMN LENGTH DIV
                dcc.Graph(
                    id='bar_graph',                                                                         # id of the graph
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Bar Graph A'},         # 'x': [what x location is the bars?],# 'Y': set: [height of bars/points]
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Bar Graph B'},
                            {'x': [1, 2, 3], 'y': [5, 2, 3], 'type': 'bar', 'name': 'Bar Graph C'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization',
                            'xaxis' : dict(
                                title='x Axis',
                                titlefont=dict(
                                family='Courier New, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'yaxis' : dict(
                                title='y Axis',
                                titlefont=dict(
                                family='Helvetica, monospace',
                                size=20,
                                color='#7f7f7f'
                            )),
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'font': {'color': colors['text']}
                        }
                    }
                ),
            ], className="four columns"),


            html.Div([          # INDIVIDUAL GRAPH COLUMN LENGTH DIV
                dcc.Graph(
                    id='line_graph',     
                    figure=fig       
                )
            ], className="eight columns"),
        ], className = "row"),

        html.Div([          # map on row 3
            html.Div([          # INDIVIDUAL GRAPH COLUMN LENGTH DIV
                dcc.Graph(
                    id='map',     
                    figure=fig_map       
                )
            ], className="eight columns"),
        ], className = "row"),

    
        






    ],  className='ten columns offset-by-one')                                      #***just added one column padding on the sides to make it look better
)

if __name__ == '__main__':
    app.run_server(debug=True)