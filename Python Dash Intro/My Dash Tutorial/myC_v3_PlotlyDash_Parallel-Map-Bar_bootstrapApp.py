# Bar and Parallel graph in one row
import dash
import dash_core_components as dcc                                                                  # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  
import plotly.graph_objects as go

import plotly.figure_factory as ff
import numpy as np
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
df['text'] = df['airport'] + '' + df['city'] + ', ' + df['state'] + '' + 'Arrivals: ' + df['cnt'].astype(str)



fig_map = go.Figure(data=go.Scattergeo(
    lon = df['long'],
    lat = df['lat'],
    text = df['text'],
    mode = 'markers',
    marker_color = df['cnt']
))

fig_map.update_layout(
    title = 'This map will show all the gas leaks reported',
    geo_scope='usa',
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
    'background': 'black',
    'text': 'white'
}

#colors of maps
fig_map.update_layout(
    plot_bgcolor = 'white',
    paper_bgcolor = 'black'
)


app.layout = html.Div(  
    html.Div(style={'backgroundColor': colors['background']}, children=[              # GLOBAL DIV                                                                
        html.Div([          # COMPONENT ROW 1 DIV
            html.H1(children='Gas Leaks',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
            }),                                                                                     # same as html.H1('Hello Dash')
            html.Div(children="Using the Dash framework",
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
                            'plot_bgcolor': 'black',#colors['background'],
                            'paper_bgcolor': 'black',#colors['background'],
                            'font': {'color': 'white'}#colors['text']}
                        }
                    }
                ),
            ], className="four columns"),


            html.Div([          # INDIVIDUAL GRAPH COLUMN LENGTH DIV
                dcc.Graph(
                    id='parallelcol',     
                    figure=fig,
                )
            ], className="eight columns"),
        ], className = "row"),

        html.Div([          # map on row 3
            html.Div([          # INDIVIDUAL GRAPH COLUMN LENGTH DIV
                dcc.Graph(
                    id='map',     
                    figure=fig_map       
                )
            ], className="twelve columns"),
        ], className = "row"),

    
        






    ],  className='ten columns offset-by-one')                                      #***just added one column padding on the sides to make it look better
)

if __name__ == '__main__':
    app.run_server(debug=True)