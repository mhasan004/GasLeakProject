""" (scraper2) SOME MODIFICATION NEEDED: I needed to scrape more census data and needed to use 2010 census data instea dof the one i used in the scraper. 
        * Didnt have time to change the scraper so added these two files to modify the file after the scape was done
        * I have already converted the scraper data to 2010 census data with additional information
        * This file takes the new reports and converts them. Simply copy and paste the edited rows to the 2010 csv
        * Do:
            1) copy paste new rows from "GasHistory_2010_ConEdisonTracts.csv" to del.csv
            2) copy paste newly modified rows from del2.csv to "GasHistory_2010_ConEdisonTracts.csv"
"""
from urllib.request import urlopen                                                      # Getting the json data from the url
import requests
import json
import pandas as pd                                                                     # To read and write csv files
import numpy as np
csvFile   = "del.csv"#"DataFiles/ConEdison/GasHistory_2010_ConEdisonTracts.csv"
csvFile2  = "del2.csv"#"DataFiles/ConEdison/GasHistory_2010_ConEdisonTracts.csv"

print("**** NEED TO DELETE THE ORIGINAL 2019 CENSUS TRACT,BLOCK AND COUNTY COLUMNS FROM THE OLD FILE - or just delete after runing this and use excel to del manually*****")
# Function to populate those expandCols
def getCensusTract(longitude, latitude,retryRun=0):                                                                 # returns an array [censusTract, CensusBlock, CountyName]
    #url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Census2010&vintage=Census2010_Census2010&format=json".format(longitude,latitude)
    if retryRun == 11:                                                                                              # Failed to get json data 11 times with this longitude and latitude so need to skip this one
        print("*****Failed 11 times to get geodata so will insert 'error'*****")
        return [str("error"), str("error"), str("error")]
    try:
        response = requests.get(url)
        dataJSON = response.json()
        data    = dataJSON["result"]

        tractNAME     = data["geographies"]["Census Tracts"][0]["NAME"]
        tractBASENAME = data["geographies"]["Census Tracts"][0]["BASENAME"]
        tractID       = data["geographies"]["Census Tracts"][0]["TRACT"]
        countyNAME    = data["geographies"]["Counties"][0]["NAME"] 
        blockGEOID =  data["geographies"]["Census Blocks"][0]["GEOID"]
        blockNAME     = data["geographies"]["Census Blocks"][0]["NAME"] 
        blockBASENAME = data["geographies"]["Census Blocks"][0]["BASENAME"]
        blockID       = data["geographies"]["Census Blocks"][0]["BLOCK"]
        # Returns: tractBASENAME, blockBASENAME, countyName, geoid, tractid and name, block id and name
        return [
            str(tractBASENAME), str(blockBASENAME), str(countyNAME), str(blockGEOID), 
            str(tractID), str(tractNAME), str(blockID), str(blockNAME)
        ]
    except:
        retryRun+=1
        print("Error on longitude, latitude: "+str(longitude)+","+str(latitude) + ".....retrying... "+str(retryRun))
        return getCensusTract(longitude, latitude,retryRun)                                                         # need to return the recursive function
    return

# A) adding empty new cols to the df
print("A Progess")
expandCols = [ "CensusTract_2010", "CensusBlock_2010", "CountyName_2010", "GEOID_2010", 
    "CensusTract_2010_ID", "CensusTract_2010_NAME", "CensusBlock_2010_ID", "CensusBlock_2010_NAME"]  
df = pd.read_csv(csvFile)                                                          # read the csv file and store to df
for col in range(0, len(expandCols)):
    df[expandCols[col]] = np.str

# B) Using census api to fill in the cols
print("B Progress")
for row in range(0,len(df)):
    retryRun = 0
    print(row)
    returnArray = getCensusTract(float(df.iloc[row]["Longitude"].item()), float(df.iloc[row]["Latitude"].item()))    # returnArray = [tractBASENAME, blockBASENAME, countyName, geoid, tract id, tract name, block id, block name]
    # Make sure the "expandCols" index and "returnArray" index are the same so it prints to right cols
    if len(expandCols) == len(returnArray):
        for colToWrite in range(0, len(expandCols)):
            df.at[row, expandCols[colToWrite]] = returnArray[colToWrite] 
    else:
        print("*** Number of col to add and values to polulate cols are not the same!! ******")
df = df.drop(columns = ['CensusBlock', 'CensusTract', 'CountyName'])
df.to_csv(csvFile2, index=False)