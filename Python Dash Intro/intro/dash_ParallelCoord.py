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
    )
])


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('my-dropdown', 'value')])

def update_output(value):
    what_city_to_graph = {                    #This is a dictinary where the keys are cities and values are the y vals for those cities 
        'NYC': [4,2,3],
        'MTL': [1, 2, 4],
        'SF': [5, 3, 6]
    }
    return {
        'data': [
            {
                'type': 'scatter',
                'y': what_city_to_graph[value],  # loading the y axis array values.
                'name': value
            },
            {
                'type': 'scatter',
                'x': [1,2,3],
                'y': what_city_to_graph['SF'],
                'value': 'SF'
            }
        ],
        'layout': {
            'title': value
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)