#pip3 install iexfinance                # get data from iex exchange
import dash
import dash_core_components as dcc      # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html     # html elements in dash app

app = dash.Dash()                       # initializes app

app.layout = html.Div(                  # Div element encloses/contains all the dash elements,graphs, etc
    html.H1(children = "Hello World")
)

if __name__ == "__main__":  # The python interperter needs to know where which file to start from. Since this is th eonly file, its the "main" file
    app.run_server(debug=True)



