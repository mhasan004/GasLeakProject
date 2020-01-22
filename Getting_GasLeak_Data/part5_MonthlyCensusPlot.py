
#%%                           
import geopandas as gp
import os
import platform
import pandas as pd
import numpy as np
# Printing the totl reports of a census tract for that month
##########################################################
# def set_pandas_display_options() -> None:
#     # Ref: https://stackoverflow.com/a/52432757/
#     display = pd.options.display

#     display.max_columns = 1000
#     display.max_rows = 1000
#     display.max_colwidth = 199
#     display.width = None
#     # display.precision = 2  # set as needed

# set_pandas_display_options()

#########################################################


shapeFile = "NY_SP/tl_2019_36_tract.shp"
csvFile = "GasHistory_ReportFrequency_Monthly.csv"
shapeDF = gp.read_file(shapeFile)                                               # Read the shape file and make a data frame
monthlyDF = pd.read_csv(csvFile)                                                 # Read the csv file and make a data frame

monthlyDF[['Month', 'Year']] = monthlyDF.MonthYear.str.split("-",expand=True)    # Splitng the "MonthYear" column into "Month", "Year" for easier querying
monthlyDF[['Year', 'CensusTract']] = monthlyDF[['Year', 'CensusTract']].apply(pd.to_numeric).astype(int)                     # Turning "Year" and "CensusTract" to numpy.int64 values so can query them (NAME col is in int while CensusTract is in float)
shapeDF[['NAME']] = shapeDF[['NAME']].apply(pd.to_numeric).astype(int)                      # Turning "NAME" - the CensusTract number to numpy.int64 values so can query them

thisMonthPlotDF = shapeDF.copy()
thisMonthPlotDF.drop(thisMonthPlotDF.index, inplace=True)                                                 # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdDF dont work


skipIndex = []
for row in range(0,len(monthlyDF)):
    if row in skipIndex:
        continue
    thisMonthsDF = monthlyDF.loc[                                                   # thisMonthsDF = df that contains all rows for that month-year
        (monthlyDF['MonthYear']  == monthlyDF['MonthYear'][row]) 
    ]
    if len(thisMonthsDF) == 0:                                                      # If these r no reports for this month-year so skip
        continue
    skipIndex.extend(thisMonthsDF.index.tolist()) 
    censusForThisMonth = thisMonthsDF.CensusTract.tolist()                                  # need to put census tracts into an array, if i use directly from thisMonthsDF i get errors when there is no 

    # print(str(type(thisMonthsDF["CensusTract"][row]))+"            "+str(thisMonthsDF["CensusTract"][row]))
    # print(np.equal(shapeDF['NAME'][0], thisMonthsDF["CensusTract"][row]      ))
    # print("                            "+monthlyDF['MonthYear'][row]+"              len: "+str(len(thisMonthsDF))+"\n"+str(censusForThisMonth))
    # print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    # for tractRow in range(0, len(censusForThisMonth)):
    #     tractShapeDF = shapeDF.loc[                                                   # this df that contains all census block shapes to make this tract
    #         np.equal(shapeDF['NAME'], censusForThisMonth[tractRow])
    #     ]  
    #     if len(tractShapeDF) == 0:
    #         print("************************************No geoid for Tract: "+str(censusForThisMonth[tractRow])) 
    #         continue
        
    #     thisMonthPlotDF = thisMonthPlotDF.append(tractShapeDF)
    # print(tractShapeDF)
    # print("--------------------------------------------------------------------------did : "+str(monthlyDF['MonthYear'][row])+"\n"+str(censusForThisMonth)+"\n")
    # # thisMonthPlotDF.plot()
    # # thisMonthPlotDF.drop(thisMonthPlotDF.index, inplace=True)                           # cleared the df so that i can do the next month
    




    # for tractRow in range(0, len(thisMonthsDF)):
    #     # print( np.equal(shapeDF['NAME'], int(thisMonthsDF["CensusTract"][tractRow])))
    #     print("-----------------------------------------------------------"+str(tractRow)+"      l:"+str(len(thisMonthsDF)))
    #     # tractShapeDF = shapeDF.loc[                thisMonthsDF["CensusTract"][tractRow]thisMonthsDF["CensusTract"][tractRow]                                   # thisMonthsDF = df that contains all rows for that month-year
    #     #     np.equal(shapeDF['NAME'], int(thisMonthsDF["CensusTract"][tractRow]))
    #     # ]  
    #     # print(type(thisMonthsDF["CensusTract"][0]))
    #     # if len(tractShapeDF) == 0:
    #     #     print("bbbbb")
    #     #     print("no geoid for tract: "+str(thisMonthsDF["CensusTract"][tractRow])) 
    #     #     continue





    #     print(len(thisMonthsDF))
        # print(tractShapeDF)
        # print("-------------" )
        # print("--------------------------------------------------------------------------------------------------------------------------------------------------------------")

    # for tractIndex in range(0, len(censusForThisMonth)):
    #     tractShapeDF = shapeDF.loc[                                                   # thisMonthsDF = df that contains all rows for that month-year
    #         (shapeDF['NAME']  == censusForThisMonth[tractIndex]) 
    #     ]   
    #     print(tractShapeDF)
    #     print("-------------" + 



    # skipy = []
    # for row2 in range(0, len(thisMonthsDF)):
    #     if row2 in skipy:
    #         continue
    #     tractn = 0
    #     one2MonthlyDF = thisMonthsDF.loc[                                                   # thisMonthsDF = df that contains all rows for that month-year
    #         (thisMonthsDF['CensusTract']  == thisMonthsDF['CensusTract'][row2]) 
    #     ]
    #     skipy.extend(one2MonthlyDF.index.tolist()) 
    #     # tractn = len(one2MonthlyDF)
    #     # if tractn >1:
    #     #     print(one2MonthlyDF)


    # print(thisMonthsDF)
    # print("----------------------")

#     monthlyDF = monthlyDF.reset_index(drop=True)                                # resetting the index of the df
#     monthlyDFArray.append(monthlyDF)                                                            # adding this month's df to the array so i can reference this later
# newShapeDF = shapeDF.copy()
# newShapeDF.drop(newShapeDF.index, inplace=True)                                                 # copied shapef df and emptied it to get empty df. idk why but making empty df with the cols of shapdf dont work
# shapeDF.plot()
# print(monthlyDFArray[len(monthlyDFArray)-1])                         














# for dfRow in range(0,len(monthlyDFArray)):
#     monthIndex = monthlyDFArray[dfRow]["Month"][0]                                              # Going through the monthlyDFArray and spiting out the month number, will use that month number to spit out the month name
#     monthName = months[monthIndex-1]
#     year = monthlyDFArray[dfRow]["Year"][0]  
#     plotTitle = "For "+monthName+" "+str(year)
    
#     tract = []                                                                                  # *****will contain all CensusTract ids for this entire months frequency data (there will be duplicates s0 need to delete them)
#     for row in range(0, len(monthlyDFArray[dfRow])):
#         tract.append(monthlyDFArray[dfRow].iloc[row]["CensusTract"])                            # This array has all the census tracts that exists in this month
    
#     for row in range(0, len(tract)):
#         newShapeDF = newShapeDF.append(shapeDF[shapeDF.NAME == str(int(tract[row]))])           # Prints all GEOID's (prints all blocks) that has this Census Tract
#     # newShapeDF.set_title(plotTitle)
#     # print(plotTitle)

#     newShapeDF.plot(cmap='rainbow')
#     print("------------------------------------------------------------------------------------"+plotTitle+"     Block in Tract:"+str(len(newShapeDF))+ "       reports# in month: "+str(len(monthlyDFArray[dfRow])))

#     print(newShapeDF)
#     newShapeDF.drop(newShapeDF.index, inplace=True) 
   
# %%

















    # if row ==0:
    #     # print(monthlyDF['CensusTract'] == 92.0)
    #     print(monthlyDF['Date'] == "2019")

    # monthlyDF.loc[  (monthlyDF['Date'][2] == "2019")   &   (monthlyDF['Date'][0] == "01")  ]

    # monthlyDF[monthlyDF['Date'].str.split("/")[0] =="1"]
    # monthlyDF = monthlyDF.loc[  
    #     (monthlyDF['Date'].str.split("/")[row][2] == "2019") 
    #     # &(monthlyDF['Date'].str.split("/")[row][1] == "01")
    # ]
    # if row >=0 and row<=100:
    #     print(
    #         str(row)+"     "+str(monthlyDF['Date'].str.split("/")[row][2] == "2019")
    #     )

    #     print("--------------------------")
    # print(monthlyDF)


    # b = monthlyDF.query('`Date`.str.endswith("2019")')
    # print("---------------------------")
    
    # monthlyDF = monthlyDF.loc[   type((monthlyDF['Date']) == monthlyDF['Date'][row])  ] 
    
    # skipIndex.extend(monthlyDF.index.tolist())
    







    # # This part is just to get the index value of the groupedDF so that i can know what index of "monthlyDF" to skip since i already have them in "groupedDF"
    # groupedDF_withIndex = pd.DataFrame(columns=csvHeader)
    # groupedDF_withIndex = monthlyDF.loc[   (monthlyDF['Date'] == monthlyDF['Date'][row]) & (monthlyDF['Hour'] == monthlyDF['Hour'][row]) & (monthlyDF['CensusTract'] == float(monthlyDF['CensusTract'][row]))    ] 
    # skipIndex.extend(groupedDF_withIndex.index.tolist())              
    
    # # Will now makw the dataframe with all the tickets with the same Date, Hour, Census track and append to outDF
    # groupedDF = pd.DataFrame(columns=csvHeader)                                                     # Making a new dataframe and letting it have the columns i want. When i append "monthlyDF" rows, the cols of "monthlyDF" will be added to it. Will finally get rid of unwanted cols with filter().     
    # groupedDF = groupedDF.append(monthlyDF.loc[                                                          # groupedDF added tickets that have the same Census Tract, Hour, and Date. Will get rid of those unwanted cols from "monthlyDF" next
    #     (monthlyDF['Date'] == monthlyDF['Date'][row]) & 
    #     (monthlyDF['Hour'] == monthlyDF['Hour'][row]) & 
    #     (monthlyDF['CensusTract'] == float(monthlyDF['CensusTract'][row]))    
    #     ], sort=False, ignore_index=True
    # ) 
    # groupedDF = groupedDF.filter(csvHeader)                                                         # Getting rid of those unwanted cols i got from "monthlyDF"

    # # Appending row to "outDF" by using small trick to get "groupDF" to one row to easily add it. Since all the rows will now have the same vals, will change the "NumberOfReports" cell and drop the other rows by droppping na's
    # groupedDF.iloc[0, groupedDF.columns.get_loc("NumberOfReports")] = len(groupedDF)
    # groupedDF = groupedDF.dropna()
    # outDF = outDF.append(groupedDF, ignore_index=True, )
















# newShapeDF = shapeDF.copy()
# newShapeDF.drop(newShapeDF.index, inplace=True)                                       # copied shapeDF monthlyDF and emptied it
# for row in range(0, len(monthlyDF)):
#     onlyConEdTracts = shapeDF[shapeDF.NAME == str(int(monthlyDF.loc[row]["CensusTract"]))] # Prints all GEOID's that has this Census Tract
#     newShapeDF = newShapeDF.append(onlyConEdTracts)

# print(newShapeDF)
# newShapeDF.plot(cmap='rainbow')
# shapeDF.plot()







