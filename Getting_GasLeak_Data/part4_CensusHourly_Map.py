#%%                            # delete the '-' to plot this block
import geopandas as gp
import os
import platform
import pandas as pd

sf = "NY_SP/tl_2019_36_tract.shp"
csvFile = "reportsPerCensusTract.csv"

dataf = pd.read_csv(csvFile)                   # Read the csv file and make a data frame
shapef = gp.read_file(sf)                      # Read the shape file and make a data frame
# for row in range(0, len(shapef)):              # not needed ADJUSTING SOME VALUES: shapef data frame has "Census Track <num>" vals so will chnage it to just numbers
#     shapeTract = float(shapef.iloc[row]["NAMELSAD"].split(" ")[2])  # The Census Tract Data is in "Census Tract <number>"
#     shapef.at[row,"NAMELSAD"] = shapeTract


newShapef = shapef.copy()
newShapef.drop(newShapef.index, inplace=True)                                       # copied shapef df and emptied it
for row in range(0, len(dataf)):
    onlyConEdTracts = shapef[shapef.NAME == str(int(dataf.loc[row]["CensusTract"]))] # Prints all GEOID's that has this Census Tract
    newShapef = newShapef.append(onlyConEdTracts)

print(newShapef)
newShapef.plot()
shapef.plot()






# %%
