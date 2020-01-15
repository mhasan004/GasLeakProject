# Census API doc: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
# census api url format: https://geocoding.geo.census.gov/geocoder/geographies/coordinatesx=longitude&y=latitude&benchmark=&vintage=&format=json
# census api url example: https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-78.8543293&y=41.6567756&benchmark=Public_AR_Current&vintage=Current_Current&format=json
    # json result of the top search given this random lat long coordinate is results: input and geographies. geographics has: 2010 census blocks, states, countries, census tracts

from urllib.request import urlopen
import json

# 1) Getting the json data from the url and putting it into a dictionary
url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-78.8543293&y=41.6567756&benchmark=Public_AR_Current&vintage=Current_Current&format=json"
response = urlopen(url)
dataJSON = json.loads(response.read())
data = dataJSON["result"]
# data dictionary form: 
#     input      { benchmark[{}], vintage[{}],location[{}]                              },
#     geographies{ 2010 Census Blocks[{}], States[{}], Countries[{}], Census Tracts[{}] }

# 2) print the census tract
censusTract = str(data["geographies"]["Census Tracts"][0]["GEOID"])[5:11] # Census tract number is the last 6 digits of the GeoID
