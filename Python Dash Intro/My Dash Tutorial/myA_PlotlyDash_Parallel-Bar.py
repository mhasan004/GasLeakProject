# Just plotting the dash bar graphs and a plotly to dash parallelcoord graph beneath it. no bootstrap
# To import plotly grpahs into dcc.Graph(). just make a fig = go.figure(...) then inside dcc.Grph() make figure = fig
import dash
import dash_core_components as dcc   # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  # 

import plotly.graph_objects as go
fig = go.Figure(data=
    go.Parcoords(
        line_color='blue',
        dimensions = list([
            dict(range = [1,5],
                 constraintrange = [1,2], # change this range by dragging the pink line
                 label = 'A', values = [1,4]),
            dict(range = [1.5,5],
                 tickvals = [1.5,3,4.5],
                 label = 'B', values = [3,1.5]),
            dict(range = [1,5],
                 tickvals = [1,2,4,5],
                 label = 'C', values = [2,4],
                 ticktext = ['text 1', 'text 2', 'text 3', 'text 4']),
            dict(range = [1,5],
                 label = 'D', values = [4,2])
        ])
    )
)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   # external cssCSS file
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    # initialize app with the external CSS file


app.layout = html.Div(
    children = [                            # children is like an array. html components and a graph.
        html.H1(children='Hello Dash A'),     # same as html.H1('Hello Dash')
        html.Div(children="Dash: A web application framework for Python."),
        dcc.Graph(
            id='bar_graph',     #id of the graph
            figure={
                'data': [
                    # 'x': [what x location is the bars?]
                    # 'Y': set: [height of bars/points]
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Bar Graph A'},
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
                    ))
                }
            }
        ),
        dcc.Graph(
            id='bar_graph2',     #id of the graph
            figure = fig
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)