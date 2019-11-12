#https://plot.ly/python/scatter-plots-on-maps/
import plotly.graph_objects as go
import pandas as pd
import dash
import dash_core_components as dcc   # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html  # 

df = pd.read_csv("airport_map.csv") # data: iata,airport,city,state,country,lat,long,count
# print(df[0]) is df[airport]
df['text'] = df['airport'] + '' + df['city'] + ', ' + df['state'] + '' + 'Arrivals: ' + df['count'].astype(str) #im inserting a key named "text" that has this string to the end of df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   # external cssCSS file
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)    # initialize app with the external CSS file


fig = go.Figure(
    data=go.Scattergeo(
        locationmode = 'USA-states',
        lon = df['long'],
        lat = df['lat'],
        text = df['text'],                          # need this for some reason
        mode = 'markers',                           # dot markers 
        marker = dict                               # these are the properties of the dots
        (                              
            size = 15,                                  # dot sizes
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(                                # the outter perimiter of the dot
                width=1,                              
                color='rgba(102, 102, 102)'
            ),
            color = df['count'],                        #***This sets the color scale***
            colorscale = 'inferno',                     # The color scale of the right and the dots
            cmin = 0,                                   # color min and max scales, cant rename these
            cmax = df['count'].max(),
            colorbar_title="Incoming flights<br>February 2011"  #the title of the bar on the right
        )
    )
)
fig.update_layout(
        title = 'Most trafficked US airports<br>(Hover for airport names)',
        geo = dict(
            scope='usa',
            projection_type='albers usa',
            showland = True,
            landcolor = "rgb(250, 250, 250)",                       # color of usa land
            subunitcolor = "rgb(217, 217, 217)",                    
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.5
        ),
    )



app.layout = html.Div(
    children = [                            # children is like an array. html components and a graph.
        html.H1(children='Hello Dash'),     # same as html.H1('Hello Dash')
        html.Div(children="Dash: A web application framework for Python."),

        dcc.Graph(
            id='bar_graph',     #id of the graph
            figure={
                'data': [
                    # 'x': [what x location is the bars?]
                    # 'Y': set: [height of bars/points]
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Bar Graph A'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Bar Graph B'},
                    {'x': [1, 2, 3], 'y': [5, 2, 3], 'type': 'bar', 'name': 'Line Graph C'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
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
                    {'x': [1, 2, 3], 'y': [5, 2, 3], 'type': 'line', 'name': 'Line Graph C'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization 2'
                }
            }
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
    fig.show()





# Valid properties:
#         autocolorscale
#             Determines whether the colorscale is a default palette
#             (`autocolorscale: true`) or the palette determined by
#             `marker.colorscale`. Has an effect only if in
#             `marker.color`is set to a numerical array. In case
#             `colorscale` is unspecified or `autocolorscale` is
#             true, the default  palette will be chosen according to
#             whether numbers in the `color` array are all positive,
#             all negative or mixed.
#         cauto
#             Determines whether or not the color domain is computed
#             with respect to the input data (here in `marker.color`)
#             or the bounds set in `marker.cmin` and `marker.cmax`
#             Has an effect only if in `marker.color`is set to a
#             numerical array. Defaults to `false` when `marker.cmin`
#             and `marker.cmax` are set by the user.
#         cmax
#             Sets the upper bound of the color domain. Has an effect
#             only if in `marker.color`is set to a numerical array.
#             Value should have the same units as in `marker.color`
#             and if set, `marker.cmin` must be set as well.
#         cmid
#             Sets the mid-point of the color domain by scaling
#             `marker.cmin` and/or `marker.cmax` to be equidistant to
#             this point. Has an effect only if in `marker.color`is
#             set to a numerical array. Value should have the same
#             units as in `marker.color`. Has no effect when
#             `marker.cauto` is `false`.
#         cmin
#             Sets the lower bound of the color domain. Has an effect
#             only if in `marker.color`is set to a numerical array.
#             Value should have the same units as in `marker.color`
#             and if set, `marker.cmax` must be set as well.
#         color
#             Sets themarkercolor. It accepts either a specific color
#             or an array of numbers that are mapped to the
#             colorscale relative to the max and min values of the
#             array or relative to `marker.cmin` and `marker.cmax` if
#             set.
#         coloraxis
#             Sets a reference to a shared color axis. References to
#             these shared color axes are "coloraxis", "coloraxis2",
#             "coloraxis3", etc. Settings for these shared color axes
#             are set in the layout, under `layout.coloraxis`,
#             `layout.coloraxis2`, etc. Note that multiple color
#             scales can be linked to the same color axis.
#         colorbar
#             plotly.graph_objects.scattergeo.marker.ColorBar
#             instance or dict with compatible properties
#         colorscale
#             Sets the colorscale. Has an effect only if in
#             `marker.color`is set to a numerical array. The
#             colorscale must be an array containing arrays mapping a
#             normalized value to an rgb, rgba, hex, hsl, hsv, or
#             named color string. At minimum, a mapping for the
#             lowest (0) and highest (1) values are required. For
#             example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`.
#             To control the bounds of the colorscale in color space,
#             use`marker.cmin` and `marker.cmax`. Alternatively,
#             `colorscale` may be a palette name string of the
#             following list: Greys,YlGnBu,Greens,YlOrRd,Bluered,RdBu
#             ,Reds,Blues,Picnic,Rainbow,Portland,Jet,Hot,Blackbody,E
#             arth,Electric,Viridis,Cividis.
#         colorsrc
#             Sets the source reference on plot.ly for  color .
#         gradient
#             plotly.graph_objects.scattergeo.marker.Gradient
#             instance or dict with compatible properties
#         line
#             plotly.graph_objects.scattergeo.marker.Line instance or
#             dict with compatible properties
#         opacity
#             Sets the marker opacity.
#         opacitysrc
#             Sets the source reference on plot.ly for  opacity .
#             determine the rendered size of marker points. Use with
#             `sizemin` and `sizemode`.
#         sizesrc
#             Sets the source reference on plot.ly for  size .
#         symbol
#             Sets the marker symbol type. Adding 100 is equivalent
#             to appending "-open" to a symbol name. Adding 200 is
#             equivalent to appending "-dot" to a symbol name. Adding
#             300 is equivalent to appending "-open-dot" or "dot-
#             open" to a symbol name.
#         symbolsrc
#             Sets the source reference on plot.ly for  symbol .

