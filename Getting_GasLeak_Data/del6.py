
#%%     
# Plotting the census tracts for all reports that appeared in a specific month                    
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np

#shapeFile = "NYU_NYC_ShapeFile/nyu_2451_34513.shp"
shapeFile = "NYU_NYC_34505_SP/nyu_2451_34505.shp"
csvFile = "GasHistory_2010_ConEdisonTracts.csv"
monthlyDF = pd.read_csv(csvFile)                                                                            # Read the csv file and make a data frame
shapeGDF = gp.read_file(shapeFile)                                                                           # Read the shape file and make a data frame
print(list(monthlyDF.columns))
print(list(shapeGDF.columns))
# #%%
# ADDING AND CHANGING DATATYPE OF COLS SO WE CAN COMPARE THEM:
shapeGDF["TotalMonthlyReport" ] = int
shapeGDF["MonthYear"] = str                                                                               # adding two new cols to shapeGDF
shapeGDF[['name']] = shapeGDF[['name']].apply(pd.to_numeric).astype(float)                                      # Turning "name" - the CensusTract number to numpy.int64 values so can query them
shapeGDF[['tractid']] = shapeGDF[['tractid']].apply(pd.to_numeric).astype(int)  
shapeGDF[['tractnum']] = shapeGDF[['tractnum']].apply(pd.to_numeric).astype(int)  
shapeGDF[['bcode']] = shapeGDF[['bcode']].apply(pd.to_numeric).astype(int) 

monthlyDF[['GEO_ID']] = monthlyDF[['GEOID_2010']].apply(pd.to_numeric).astype(int)    # Turning "Year" and "CensusTract" to numpy.int64 values so can query them (name col is in int while CensusTract is in float)
# monthlyDF[['Month', 'Year']] = monthlyDF.MonthYear.str.split("-",expand=True)                               # Splitng the "MonthYear" column into "Month", "Year" for easier querying
# monthlyDF[['Year']]        = monthlyDF[['Year']].apply(pd.to_numeric).astype(int)    # Turning "Year" and "CensusTract" to numpy.int64 values so can query them (name col is in int while CensusTract is in float)

print(list(monthlyDF.columns))
print(list(shapeGDF.columns))
print(monthlyDF)
print("-------------")
print(shapeGDF)

# 
# SEE WHAT TRACTS ARE IN CONED SITE BUT NOT IN THE SHAPE FILE:
conSet = set()
shpSet = set()
for i in range(0, len(monthlyDF)):
    # print(monthlyDF.iloc[i]["GEOID_2010"])
    z = int(str(monthlyDF.iloc[i]["GEOID_2010"])[0:11])
    # print(z)
    # print(shapeGDF.iloc[i]["tractnum"])
    conSet.add(z)
    # print()
for i in range(0, len(shapeGDF)):
    shpSet.add(shapeGDF.iloc[i]["tractid"])
conSet = list(conSet)
shpSet = list(shpSet)
conSet.sort()
noneCount = 0
s=""
for i in range(0, len(conSet)):
    if conSet[i] not in shpSet:
        s=s+str(conSet[i])+", "
        noneCount = noneCount +1
print(s)
print("ConEd Tract Number:     "+str(len(conSet)))
print("Shapefile Tract Number: "+str(len(shpSet)))
print("Mising tracts: "+str(noneCount))
