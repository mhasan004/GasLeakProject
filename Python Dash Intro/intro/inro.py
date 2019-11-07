# Tutorial: https://www.youtube.com/watch?v=NM8Ue4znLP8&list=PLCDERj-IUIFCaELQ2i7AwgD2M6Xvc4Slf&index=2
# pip3 install iexfinance                # get data from iex exchange

import dash
import dash_core_components as dcc      # has a component for every HTML tag (html.H1() puts the string in a h1 html tag for ex)
import dash_html_components as html     # html elements in dash app

from iexfinance.stocks import get_historical_data                    # iex data
import datetime                         # to get start and end dates
from dateutil.relativedelta import relativedelta # creating fix time frame ranges because iex finance only support 5 years from todays date or  their api will give error

start = datetime.datetime.today() - relativedelta(years=5) # start date = 5 days from todays date
end  = datetime.datetime.today()     
dataFrame = get_historical_data("GE", start=start, end=end, output_format="pandas")       
print(dataFrame.head())
# app = dash.Dash()                       # initializes app

# app.layout = html.Div(                  # Div element encloses/contains all the dash elements,graphs, etc
#     html.H1(children = "Hello World")
# )

# if __name__ == "__main__":  # The python interperter needs to know where which file to start from. Since this is th eonly file, its the "main" file
#     app.run_server(debug=True)



