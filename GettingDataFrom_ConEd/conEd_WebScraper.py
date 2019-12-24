from lxml import html
import requests

page = requests.get('https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&')
print(page)









