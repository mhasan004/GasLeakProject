# Using the con ed report data to make hourly and monthly freq report count csv files:
from urllib.request import urlopen                                                      # Getting the json data from the url
import requests
import json
import pandas as pd                                                                     # To read and write csv files
import numpy as np
import csv
csvFile         = "GasHistory_2010_ConEdisonTracts.csv"
csvHourlyFile   = "GasHistory_2010_ReportFrequency_Hourly.csv"                                                             # In PART C we will turn the ticket history data to hourly data
csvMonthlyFile  = "GasHistory_2010_ReportFrequency_Monthly.csv"                                                             # In PART C we will turn the ticket history data to hourly data

# PART C1 FUNCTION: Make Hourly reports from the gas leak history csv file
def turnTickeyHistory_toHourlyReport():
    global csvFile
    global csvHourlyFile
    csvOutHasData = False                                                                                           # Does the out file have data already? if so can get it and use it and modify it
    conDF = pd.read_csv(csvFile)                                                                                     # Read Tracts file
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # ADDING NEW COLS: outDF WILL HAVE ALL THESE NEW COLS. NEED TO ADD THEM TO conDF so it can have it.adding new col to outDF so need to add it to conDF
    conDF["MonthYear"] = str
    conDF["NumberOfReports"] = int      
    conDF["Year"] = int
    conDF["GEOID_list"] = str
    conDF["CensusBlockID_list"] = str
    conDF["Zipcode_list"] = str
    conDF["Ticket_list"] = str

    # Adding Month, Day, Year cols and sorting by it
    conDF[['Month','Day', 'Year']] = conDF.Date.str.split("/",expand=True)                                    # Splitng the "Date" column into "Month", "Day", "Year" for easier querying
    conDF[['Month','Day', 'Year']] = conDF[['Month','Day', 'Year']].apply(pd.to_numeric)                      # Turning "Month", "Day", "Year" to numeric values so can query them
    conDF = conDF.sort_values(by=['Year', 'Month', 'Day'], ascending=False)
    conDF = conDF.reset_index(drop=True)  

    # LISTING COLS I WANT FOR outDF: adding the conDF data to outDF
    csvHeader = ["MonthYear","Date", "Year", "Hour", "CensusTract_2010","NumberOfReports", "CensusTract_2010_ID", "CensusTract_2010_NAME",
        "CountyName_2010", "GEOID_list", "CensusBlockID_list", "Zipcode_list", "Ticket_list"
        ]                                                             # My new csv need these headers        
    csvOutClear = open(csvHourlyFile, "w")
    csvOutClear.truncate()                                                                                          # deleting everything in the file (will delete this code once i figure out how to update existing file)
    
    with open(csvHourlyFile, 'r') as hourlyFile:                                                                       # Open the csv File so we can read it
        csvTable = [row for row in csv.DictReader(hourlyFile)]
        if len(csvTable) == 0:                                                                                      # a) csv is empty so add my header: ['Date', 'Hour', 'CensusTract_2010', 'NumberOfReports']
            with open(csvHourlyFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
        else:
            csvHeader=list(pd.read_csv(csvHourlyFile).columns)                                                      # b) Since the csv already had data, it means i will append new data to it so just use the header of that csv file.
            csvOutHasData = True                                                                                    # There is data here, after i make a new DF using the tract csv i have, will go through the other csv and increment or keep the report counts

    outDF = pd.DataFrame(columns=csvHeader)                                                                         # making newDF with the cols i want. This will be appended to the other csv
    skipIndex = [] 
    print("          Turning the Gas Leak Report csv into hourly reports DF...")
    for row in range(0,len(conDF)):
        if row in skipIndex:
            continue
        # This part is just to get the index value of the groupedDF so that i can know what index of "conDF" to skip since i already have them in "groupedDF"
        groupedDF = pd.DataFrame(columns=csvHeader)
        groupedDF = conDF.loc[   
            (conDF['Date'] == conDF['Date'][row]) & 
            (conDF['Hour'] == conDF['Hour'][row]) & 
            (conDF['CensusTract_2010_ID'] == float(conDF['CensusTract_2010_ID'][row]))    ] 
        skipIndex.extend(groupedDF.index.tolist())    
        groupedDF = groupedDF.reset_index(drop=True)      
        
        # Now that i hae the mini df for each hour per census tract, will input list of geoids, and blocks for that hour in that census tract
        blockList = []
        geoidList = []
        ticketList = []
        zipcodeList = []
        for blockRow in range(0,len(groupedDF)):
            geoidList.append(groupedDF.iloc[blockRow]["GEOID_2010"])
            blockList.append(groupedDF.iloc[blockRow]["CensusBlock_2010_ID"])
            zipcodeList.append(groupedDF.iloc[blockRow]["Zip"])
            ticketList.append(groupedDF.iloc[blockRow]["TicketNumber"])
        groupedDF = groupedDF.filter(csvHeader)                                                                     # Getting rid of those unwanted cols i got from "conDF"

        # Appending row to "outDF" by using small trick to get "groupDF" to one row to easily add it. Since all the rows will now have the same vals, will change the "NumberOfReports" cell and drop the other rows by droppping na's
        # Since the groupedDF was new and the conDF both didnt have "NumberOfReorts" column, it was exclused, will now add it back!
        groupedDF.iloc[0, groupedDF.columns.get_loc("GEOID_list")] = str(geoidList)
        groupedDF.iloc[0, groupedDF.columns.get_loc("CensusBlockID_list")] = str(blockList)
        groupedDF.iloc[0, groupedDF.columns.get_loc("Zipcode_list")] = str(zipcodeList)
        groupedDF.iloc[0, groupedDF.columns.get_loc("Ticket_list")] = str(ticketList)
        groupedDF.iloc[0, groupedDF.columns.get_loc("NumberOfReports")] = len(groupedDF)                           # This DF will have the same rows but NumberOFRep and Year will be na, will only push the first row after modifying it and delte na rows.
        groupedDF.iloc[0, groupedDF.columns.get_loc("Year")] = int(groupedDF.iloc[0]["Date"].split("/")[2])
        groupedDF.iloc[0, groupedDF.columns.get_loc("MonthYear")] = months[int(groupedDF.iloc[0]["Date"].split("/")[0])-1] + "-" + groupedDF.iloc[0]["Date"].split("/")[2]

        groupedDF = groupedDF.drop(groupedDF.index[1:len(groupedDF)])                                               # **taking out the first orw and appending it
        outDF = outDF.append(groupedDF, ignore_index=True, sort = False)
    outDF = outDF.reset_index(drop=True)
    print("          Printing hourly report DF to "+csvHourlyFile+"...")
    with open(csvHourlyFile,'a') as outCSV:                                                                         # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))
    









# PART C2 FUNCTION: Trung the Hourly Frequency report into monthly report
def turnTickeyHistory_toMonthlyReport():
    global csvFile
    global csvMonthlyFile
    csvOutHasData = False                                                                                           # Does the out file have data already? if so can get it and use it and modify it
    conDF = pd.read_csv(csvFile)                                                                                     # Read Tracts file
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    # Creating headers for the output monthly file: 
    csvHeader = ["MonthYear", "CensusTract_2010", "TotalReports", "CensusTract_2010_ID", "CensusTract_2010_NAME",
        "CountyName_2010", "GEOID_SCT", "CensusBlockID_list", "Zipcode_list", "Ticket_list", "Classification_list", "Month", "Year"
    ]
    outDF = pd.DataFrame(columns=csvHeader)                                                                         # making newDF with the cols i want. This will be appended to the other csv
    
    # Clearing the output monthly csv file:
    csvOutClear = open(csvMonthlyFile, "w")
    csvOutClear.truncate()    
    with open(csvMonthlyFile, 'w', newline='') as outf:
        writer = csv.writer(outf)
        writer.writerow(csvHeader)

    # geoID = str(361190068022001) #36, 119, 006800
    # geoID_state = geoID[0:2]    # state id is first 2 digits of geoid
    # geoID_county = geoID[2:5]   # county id is next 3 digits of geoid
    # geoID_tract = geoID[5:11]   # census tract is next 6 digits of geoid

    
    # Adding new cols to input df so can merge common cols
    conDF["MonthYear"] = str
    conDF["TotalReports"] = int
    conDF["GEOID_SCT"] = int
    conDF["CensusBlockID_list"] = str
    conDF["Zipcode_list"] = str
    conDF["Ticket_list"] = str
    conDF["Classification_list"] = str

    # Adding Month, Day, Year cols and sorting by it
    conDF[['Month','Day', 'Year']] = conDF.Date.str.split("/",expand=True)                                    # Splitng the "Date" column into "Month", "Day", "Year" for easier querying
    conDF[['Month','Day', 'Year']] = conDF[['Month','Day', 'Year']].apply(pd.to_numeric)                      # Turning "Month", "Day", "Year" to numeric values so can query them
    conDF = conDF.sort_values(by=['Year', 'Month', 'Day'], ascending=False)
    conDF = conDF.reset_index(drop=True)  

    # Populating the GEOID_SCT column with the state,county,tract unique id!
    for row in range(0, len(conDF)):
        geoid_sct = str(conDF.iloc[row]["GEOID_2010"])[0:11]
        conDF.iloc[row, conDF.columns.get_loc("GEOID_SCT")] = int(geoid_sct)
    
    skipIndex = []                                                                                                  # Array that stores the indexes i will skip. Will query for reports in the same month, the resulting rows will be appeneded to be skipped
    monthlyDFArray = []                                                                                             # For each month, there will be a dataframe of reports, will store each month's dataframe to this index
    print("          Turning csv to Monthly DFs...")
    for row in range(0,len(conDF)):
        if row in skipIndex:
            continue
        monthlyDF = conDF.loc[                                                                                   # Querying for all rows that has took place in the same year and month - aka df of monthly reports
            (conDF['Year']  == conDF['Year'][row]) &
            (conDF['Month'] == conDF['Month'][row]) 
            # (conDF['GEOID_SCT'] == conDF['GEOID_SCT'][row])    ] 
        ]
        skipIndex.extend(monthlyDF.index.tolist())                                                                  # Since i have these rows already, can skip them
        # monthlyDF = monthlyDF.filter(csvHeader)
        monthlyDF = monthlyDF.reset_index(drop=True)                                                                # resetting the index of the df (didnt do this in the other function)
        monthlyDFArray.append(monthlyDF)                                                                            # adding this month's df to the array so i can reference this later


    # a) Going through each monthly DF and making small temporary DF for each CensusTract for that month and outputing only one row for each censustract for each month that contaisn the totla report of that census tract for that month
    for dfRow in range(0,len(monthlyDFArray)):                                                                      # Going through each monthly DF that coneains a hourly reports of the month
        # Making a string that has the Month and year
        monthIndex = monthlyDFArray[dfRow]["Month"][0]                                                              # Going through the monthlyDFArray and spiting out the month number, will use that month number to spit out the month name
        monthName = months[monthIndex-1]
        year = monthlyDFArray[dfRow]["Year"][0]  
        strMonthYr = monthName+"-"+str(year)
        thisMonth = pd.DataFrame(columns=csvHeader)                                                                         # making newDF with the cols i want. This will be appended to the other csv
        
        #b) each row of the monthly df: Going through the month DF's rows and making small temporary DF to store each census tract. will count how any for that tract for this month
        reportSum = 0
        
        skipIndexMonthlyTract = []
        for row in range(0, len(monthlyDFArray[dfRow])):                                                             
            if row in skipIndexMonthlyTract:
                continue
            thisMonthsTractDF = monthlyDFArray[dfRow].loc[                                                             # Querying for all rows that has same census tract - this new DF contains the same census tract rows of the month
                monthlyDFArray[dfRow]['GEOID_SCT']  == monthlyDFArray[dfRow]['GEOID_SCT'][row]
            ]
            skipIndexMonthlyTract.extend(thisMonthsTractDF.index.tolist())                                             # Since I am doing these tracts, can skip them next time
            reportSum = len(thisMonthsTractDF)                                                    # Summing up the report count fileds of each report of that census tract for this month
            thisMonthsTractDF = thisMonthsTractDF.reset_index(drop=True)
            thisMonthsTractDF.iloc[0, thisMonthsTractDF.columns.get_loc("TotalReports")] = reportSum                          # This DF will have the same rows but NumberOFRep and Year will be na, will only push the first row after modifying it and delte na rows.
            thisMonthsTractDF.iloc[0, thisMonthsTractDF.columns.get_loc("MonthYear")] = strMonthYr 

            # Now that i hae the mini df for each census tract for the month, will input list of geoids, and blocks for that hour in that census tract
            blockList = []
            ticketList = []
            zipcodeList = []
            classificationlist = []
            for mtRow in range(0, len(thisMonthsTractDF)):
                blockList.append(thisMonthsTractDF.iloc[mtRow]["CensusBlock_2010_ID"])
                zipcodeList.append(thisMonthsTractDF.iloc[mtRow]["Zip"])
                ticketList.append(thisMonthsTractDF.iloc[mtRow]["TicketNumber"])
                classificationlist.append(thisMonthsTractDF.iloc[mtRow]["ClassificationType"])
            # populating the list columns
            thisMonthsTractDF.iloc[0, thisMonthsTractDF.columns.get_loc("CensusBlockID_list")]  = str(blockList)
            thisMonthsTractDF.iloc[0, thisMonthsTractDF.columns.get_loc("Zipcode_list")]        = str(zipcodeList)
            thisMonthsTractDF.iloc[0, thisMonthsTractDF.columns.get_loc("Ticket_list")]         = str(ticketList)
            thisMonthsTractDF.iloc[0, thisMonthsTractDF.columns.get_loc("Classification_list")] = str(classificationlist)
            
            thisMonthsTractDF = thisMonthsTractDF.filter(csvHeader)                                                                     # Getting rid of those unwanted cols i got from "conDF"\
            thisMonthsTractDF = thisMonthsTractDF.drop(thisMonthsTractDF.index[1:len(thisMonthsTractDF)])                                               # **taking out the first orw and appending it
            thisMonth = thisMonth.append(thisMonthsTractDF)
        outDF = outDF.append(thisMonth)
    outDF = outDF.sort_values(by=["Year", "Month", "GEOID_SCT"], ascending=False)
    outDF = outDF.reset_index(drop=True)
    print("          Writing to monthly csv file...")
    with open(csvMonthlyFile,'a') as outCSV:                                                                         # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))






















turnTickeyHistory_toHourlyReport()
# turnTickeyHistory_toMonthlyReport()