import requests                     # Getting html data
from bs4 import BeautifulSoup       # Parse the HTML data
import pandas as pd                 # 

url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&'
res = requests.get(url)
html_data = res.content

soup = BeautifulSoup(html_data, 'html.parser')  # the HTML data to parse
text = soup.find_all(text=True)

jsonStr = ''                                     # turning to string
for t in text:
	jsonStr += '{} '.format(t)

jsonScraped = []
jsonScraped = pd.read_json(jsonStr, orient='records') # Turning the json string to a dictionary
print(jsonScraped["TicketNumber"][0])





