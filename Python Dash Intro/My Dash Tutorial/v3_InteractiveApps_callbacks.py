import dash
import dash_core_components as dcc                                                                  # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  

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
            html.H1(children='Hello Dash',
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
            ], className="six columns"),
            html.Div([          # INDIVIDUAL GRAPH COLUMN LENGTH DIV
                dcc.Graph(
                    id='line_graph',     
                    figure={
                        'data': [
                            {'x': [1, 2, 3, 4, 5, 6], 'y': [4, 1, 2,5,6,2], 'type': 'line', 'name': 'Line Graph A'},
                            {'x': [1, 2, 3, 4, 5, 6], 'y': [2, 4, 5,3,5,7], 'type': 'line', 'name': 'Line Graph B'},
                            {'x': [1, 2, 3, 4, 5, 6], 'y': [5, 2, 3,2,8,3], 'type': 'line', 'name': 'Line Graph C'},
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
                )
            ], className="six columns"),
        ])
    ],  className='ten columns offset-by-one')                                      #***just added one column padding on the sides to make it look better
)

if __name__ == '__main__':
    app.run_server(debug=True)