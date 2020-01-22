
#%%     
# Plotting the census tracts for all reports that appeared in a specific month                    
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np


shapeFile = "NY_SP/tl_2019_36_tract.shp"
csvFile = "GasHistory_ReportFrequency_Monthly.csv"
shapeDF = gp.read_file(shapeFile)                                                                           # Read the shape file and make a data frame
monthlyDF = pd.read_csv(csvFile)                                                                            # Read the csv file and make a data frame

monthlyDF[['Month', 'Year']] = monthlyDF.MonthYear.str.split("-",expand=True)                               # Splitng the "MonthYear" column into "Month", "Year" for easier querying
monthlyDF[['Year', 'CensusTract']] = monthlyDF[['Year', 'CensusTract']].apply(pd.to_numeric).astype(int)    # Turning "Year" and "CensusTract" to numpy.int64 values so can query them (NAME col is in int while CensusTract is in float)
shapeDF[['NAME']] = shapeDF[['NAME']].apply(pd.to_numeric).astype(int)                                      # Turning "NAME" - the CensusTract number to numpy.int64 values so can query them
shapeDF.plot()

thisMonthPlotDF = shapeDF.copy()
thisMonthPlotDF.drop(thisMonthPlotDF.index, inplace=True)                                                   # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdDF dont work


skipIndex = []
count = 0
for row in range(0,len(monthlyDF)):
    if row in skipIndex:
        continue
    thisMonthsDF = monthlyDF.loc[                                                                           # thisMonthsDF = df that contains all rows for that month-year
        (monthlyDF['MonthYear']  == monthlyDF['MonthYear'][row]) 
    ]
    if len(thisMonthsDF) == 0:                                                                              # If these r no reports for this month-year so skip
        continue
    skipIndex.extend(thisMonthsDF.index.tolist()) 
    censusForThisMonth = thisMonthsDF.CensusTract.tolist()                                                  # need to put census tracts into an array, if i use directly from thisMonthsDF i get errors when there is no 
    
    for tractRow in range(0, len(censusForThisMonth)):
        tractShapeDF = shapeDF.loc[                                                                         # this df that contains all census block shapes to make this tract
            np.equal(shapeDF['NAME'], censusForThisMonth[tractRow])
        ]  
        if len(tractShapeDF) == 0:
            print("************************************ No geoid for Tract: "+str(censusForThisMonth[tractRow])) 
            continue
        thisMonthPlotDF = thisMonthPlotDF.append(tractShapeDF)
    thisMonthPlotDF = thisMonthPlotDF.reset_index(drop=True)                                                # reset the index
    count=count+1   
    print(thisMonthPlotDF.NAME)                                                                             # * Print the list of geo id/ census tract that are needed to make the census tracts for this month
    print("Census Tracs to print:    "+str(censusForThisMonth))                                             # * Print the list of census tracts for this month
    print("--------------------------------------------------------------------------did : "+str(monthlyDF['MonthYear'][row])+"      NumberOfBlocksToPrint: "+str(len(thisMonthPlotDF.NAME))+"     GraphID: "+str(count))
    thisMonthPlotDF.plot()
    thisMonthPlotDF.drop(thisMonthPlotDF.index, inplace=True)                                               # Cleared the df so that i can do the next month
    

# %%
