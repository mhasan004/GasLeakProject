# PART 2 CODE AFER CON ED SCRAPER
# a) make a new csv that has the: censusTract, date, hour, report count for that tract for that hour
# Census API doc:         https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf
# census api url format:  https://geocoding.geo.census.gov/geocoder/geographies/coordinatesx=latitude&y=longitude&benchmark=&vintage=&format=json
# census api url example: https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=-78.8543293&y=41.6567756&benchmark=Public_AR_Current&vintage=Current_Current&format=json
    # json result of the top search given this random lat long coordinate is results: input and geographies. geographics has: 2010 census blocks, states, countries, census tracts


from urllib.request import urlopen                                                      # Getting the json data from the url
import json
import pandas as pd                                                                     # To read and write csv files
import time                                                                             # maybe api calls will help if i slow a bit

csvConEdFile  = "GasHistory_ConEdisonTracks.csv"
################################################################################### GETTING CENSUS DATA FROM COORDS AND ADDING TO CSV ####
# FUNCTION: Get Census Tract from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file 
def getCensusTract(longitude, latitude,retryRun=0):                                     # returns an array [CensusTrack, CensusBlock, CountyName]
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?y={0}&x={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
    response = urlopen(url)
    dataJSON = json.loads(response.read())
    data = dataJSON["result"]
    if retryRun == 11:                                                                  # Failed to get json data 11 times with this longitude and latitude so need to skip this one
        print("failed 11 times")
        return [str("error"), str("error"), str("error")]
    try:
        track = data["geographies"]["Census Tracts"][0]["BASENAME"]
        block = data["geographies"]["2010 Census Blocks"][0]["BLOCK"]
        county = data["geographies"]["Counties"][0]["NAME"] 
        return [str(track), str(block), str(county)]
    except:
        retryRun+=1
        print("******** Error on longitude, latitude: "+str(longitude)+","+str(latitude) + " ------ retrying "+str(retryRun))
        return getCensusTract(longitude, latitude,retryRun)                             # *****need to return the recursive function

# a) Will modify GasHistory_ConEdison.csv to have the CensusTract, CensusBlock, and CountyName columns
censusTrack = []
censusBlock = []
countyName = []
df = pd.read_csv(csvConEdFile)                                                          # read the csv file and store to df
for row in range(0,len(df)):
    retryRun = 0
    # b) using the lat and long coords of each entry to find the census data and adding to the respective arrays to add to csv col later
    returnArray = getCensusTract(float(df.loc[row]["Longitude"].item()), float(df.loc[row]["Latitude"].item()))
    censusTrack.append(returnArray[0])
    censusBlock.append(returnArray[1])
    countyName.append(returnArray[2])

# c) Will make 3 new columns and will fill them up using the 3 census arrays
df['CensusTrack'] = censusTrack          
df['CensusBlock'] = censusBlock        
df['CountyName']  = countyName      
df.to_csv(csvConEdFile)                                

#########################################################################################################################################

