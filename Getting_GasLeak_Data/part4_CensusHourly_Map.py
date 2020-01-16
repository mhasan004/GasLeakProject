#-%%                            # delete the '-' to plot this block
import geopandas as gp
import os
import platform
import pandas as pd

sf = "NY_SP/tl_2019_36_tract.shp"
csvFile = "reportsPerCensusTract.csv"

dataf = pd.read_csv(csvFile)                   # Read the csv file and make a data frame
shapef = gp.read_file(sf)                      # Read the shape file and make a data frame
for row in range(0, len(shapef)):              # ADJUSTING SOME VALUES: shapef data frame has "Census Track <num>" vals so will chnage it to just numbers
    shapeTract = float(shapef.iloc[row]["NAMELSAD"].split(" ")[2])  # The Census Tract Data is in "Census Tract <number>"
    shapef.at[row,"NAMELSAD"] = shapeTract

print(shapef)


# shapef.plot()








