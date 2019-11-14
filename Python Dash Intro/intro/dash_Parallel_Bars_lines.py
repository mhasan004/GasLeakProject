import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
    dcc.Graph(
        id='graph',
        config={
            'showSendToCloud': True,
            'plotlyServerURL': 'https://plot.ly'
        }
    ),
    dcc.Graph(
        id='scatter_plot',     #id of the graph
        figure={
            'data': [
                # 'x': [what x location is the bars?]
                # 'Y': set: [height of bars/points]
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Bar Graph A'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Bar Graph B'},
                {'x': [1, 2, 3], 'y': [5, 2, 3], 'type': 'bar', 'name': 'Line Graph C'},
            ],
            'layout': {
                'title': 'Dash Data Visualization 2'
            }
        }
     )
])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    what_city_to_graph = {
        'NYC': [3, 6, 7, 6, 7, 8],#[[1,2,3],[4, 5, 6],[7, 8, 9]],
        'MTL': [1, 2, 4, 4, 3, 1],
        'SF':  [5, 3, 6, 7, 6, 9]
    }
    return {
        'data': [
            {
                'type': 'scatter',
                'x': [1,2,3,4,5,6],
                'y': what_city_to_graph['NYC'],
                'name': 'NYC'
            },
            {
                'type': 'scatter',
                'x': [1,2,3,4,5,6],
                'y': what_city_to_graph['SF'],
                'name': 'SF'
            },
            {
                'type': 'scatter',
                'x': [1,2,3,4,5,6],
                'y': what_city_to_graph['MTL'],
                'name': 'MT',
            }
        ],
        'layout': {
            'title': value
        }
    }







if __name__ == '__main__':
    app.run_server(debug=True)