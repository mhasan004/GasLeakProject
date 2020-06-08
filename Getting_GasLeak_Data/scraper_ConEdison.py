
# Variables to change:  csvFile, csvHourlyFile, csvMonthlyFile, PATH_OF_GIT_REPO

# Scraper v4: Will periodicly scrape the con edison website to find new gas leak reports, then use the Census Bureau API to find Census Data of those locations and append to my csv file. Will then read the file and make a new csv file to trck reports per hour per Census Tract per day and create a map.
# Part A (section 1 to 4, 6, 8): Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use
    # In the ConEdison Gas Leak Report Map, each report in the map represents a gas leak report. Each report has these seven keys: TicketNumber, Latitude, Longitude, Zipcode, Classification Type, Date Reported, Last Inspected.
    # a) We need to constantly add new repots to out list so what tickets do we currently have? read the ticket col of the "csvConEdFile" and add the tickets to "ticketSet"
    # b) Scrape the JSON html response and using pandas to put the contents into a dataframe called "jsonDF"
    # c) See if there is a new report, if there is create a new DF that stores info for those new tickets: 
        # Read the csv file and make a dataframe with pandas. Now compare the "TicketNumber" columns of both the "csvDF" and "jsonDF" using left merge and store it as a new DF - "mergedDF" -  which has the info of all the tickets and has a new column called "_merged" which shows what ticket are in both DF and what tickets are in only json response. 
        # Filter "mergedDF" where "_merged" col = ""left_only" (new tickets not in file) and print the list of ticket names to an array - "newTicketsArray" 
        # Create a new DF - "newTicketDF" - which will have the columns of my current csv file. Will use "newTicketArray" to go through the "jsonDf" and add the rows to "newTicketDF" so i have a DF that has all the new tickets
    # d) If there is a new report, add append the keys of that report into "csvConEdFile" and push the latest changes to github
# Part B (section 5):  Will edit the csv to have new columns for the Census Tract, Census Block, County Name and the hour only
    # Will use the census bureau api to get census data from the lat and lon coords using this url request:  https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=LONGITUDE&y=LATITUDE&benchmark=Public_AR_Current&vintage=Current_Current&format=json
# Part C (section 7): Will create a new csv that lists the reports per census tract per hour for that day. Headers: Date, Hour, CensusTract, NumberOfReports. Will use this new csv to create the number of reports for that month

import json
import csv
import pandas as pd                                                                                                 # to read csv file and store conent into a data frame. To turn json response string into a dataframe
import datetime,re                                                                                                  # to turn Microsoft JSON date /Date()/ to normal date
import requests                                                                                                     # Getting html data
from bs4 import BeautifulSoup                                                                                       # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler                                                       # Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                                                                                                # (GitPython) To push changes to gh

 # SETTING UP GLOBAL VARIABLES: need to change the first eight variables below
csvFile         = "DataFiles/ConEdison/GasHistory_2010_ConEdisonTracts.csv"
csvHourlyFile   = "DataFiles/ConEdison/GasHistory_2010_ReportFrequency_Hourly.csv"                                                             # In PART C we will turn the ticket history data to hourly data
csvMonthlyFile  = "DataFiles/ConEdison/GasHistory_2010_ReportFrequency_Monthly.csv"                                                             # In PART C we will turn the ticket history data to hourly data

jsonFile = "SOME_JSON_FILE.json"                                                                                    # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&'                                          # Url to scrape JSOn data from
dropCol = True                                                                                                      # If you want to drop a column, specify which ones in step 2 in WebscraperJsonToCSV()
replaceColWith = ["Date", "Time", "Hour"]#, "CensusTract", "CensusBlock", "CountyName" ]                              # Replacing column DateReported with these "Date", "Time", "Hour and Made 3 more cols for Part 2 Census data

PATH_OF_GIT_REPO = r'/home/pi/repositories/gh/GasLeakProject'                                                       # the path to the .git file (.git location on my raspberry pi)
# PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject'                                                  # the path to the .git file (.git location on my Laptop)
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'                                                               # the commmit message when it is pushed
scrapingCount = 0                                                                                                   # Just counting how many times i have scraped the website while this was running
csvreadCount = 0

# GIT PUSH FUNCTION: Setting up function to automatically push changes to github when there is a new ticket so that I can have access to the latest chnages
def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    try:
        repo.remotes.origin.pull()                                                                                  # try pulling new changes from the github repo (if there are any) so i can push changes
    except:
        print("     Couldnt pull from repo\n")
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    try:
        origin.push()                                                                                               # try pushing the changes to github
        print("     ******** PUSHED TO GITHUB for Run " + str(scrapingCount)+"********\n")
    except:
        print('     Some error occured while pushing the code\n')  

# FUNCTION TO TURN MICROSOFT JSON DATE TO mm/dd/yyyy AND TIME: returns ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
def turnToDateTimeHr(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    dateRaw = datetime.datetime.fromtimestamp(int(TimestampUtc))
    dateFormatted = str(dateRaw.strftime('%m/%d/20%y %I:%M %p'))                                                    # The datetime is of form: "mm/dd/tt hh:mm AM/PM"
    dateTimeSplit = dateFormatted.split(" ")                                                                        # ["mm/dd/yyyy", "hh:mm", "AM/PM"]
    date = dateTimeSplit[0]                                                                                         # Isolated the date string: "mm/dd/yyyy"
    time = dateTimeSplit[1] + " " + dateTimeSplit[2]                                                                # Isolated the time string: "hh:mm AM/PM"
    hour = time.split(" ")[0].split(":")[0] + " " + dateTimeSplit[2]                                                # Isolated the hour string: "hh AM/PM"   (will need for part 2)
    dateTimeHr = [date, time, hour]                                                                                 # ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
    return (dateTimeHr)                                                                

# PART B FUNCTION: Returns: TractBASENAME, BlockBASENAME, CountyName, Geoid, TractID, TrackID Name, BlockID, Block Name]. from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file 
def getCensusTract(longitude, latitude,retryRun=0):                                                                 # returns an array [censusTract, CensusBlock, CountyName]
    #url= "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
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
    print("     Turning the Gas Leak Report csv into Hourly Frequency Reports DF...")
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
    print("     .....Writing Hourly Frequency Report DF to "+csvHourlyFile+"...")
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
    print("     Turning the Gas Leak Report csv into Monthly Frequency Reports DF...")
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
    print("     .....Writing Monthly Frequency Report DF to "+csvMonthlyFile+"...")
    with open(csvMonthlyFile,'a') as outCSV:                                                                         # Turning the DF into csv and appending the new data to the file
        outCSV.write(outDF.to_csv(header=False, index=False))



# THE SCHEDULER WILL RUN THIS MAIN FUNCTION EVER X SECONDS/MINUTES/HOURS
def WebscraperJsonToCSV():  
    global scrapingCount                                                                                            # Setting up the web scraping global iteration counter for debugging purposes
    global csvReadCount
    scrapingCount = scrapingCount + 1
    scheduler.pause()           #*****pausing the sceduler
    
    # 1) GET JSON DATA: Webscrape the html response which is usually just the JSON data from the url and add to the JSON Dataframe: 
    # jsonDF = pd.read_json(jsonFile, orient='records')                                                             # If im getting data from json file, comment out the rest of this section.
    try:
        res = requests.get(url)
        html_data = res.content                                                                                     # Getting the HTML JSON data from the url 
        soup = BeautifulSoup(html_data, 'html.parser')                                                              # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
        text = soup.find_all(text=True)                                                                             # Getting all the text thats in the soup
        jsonStr = ''                                                                                                # turning text to string from so i can use pandas to turn it to a dataframe
        for t in text:
            jsonStr += '{} '.format(t)
        jsonDF = pd.read_json(jsonStr, orient='records')                                                            # Turning the json string to a pandas dataframe
        print("Run Starting " + str(scrapingCount) + "       Reports Scraped: "+str(len(jsonDF)))
    except:
        print("         Couldnt get the json data so will re-run function. This is Run "+ str(scrapingCount))
        scheduler.resume() #****resuming the job 
        return WebscraperJsonToCSV()
    
    # 2) MODIFY CSV FILE: 
        # a) CSV IS EMPTY: print the the headers I want. 
        # b) CSV NOT EMPTY: Get the header and that is what we will work with. Im also droping columns from json DF and adding new col titles to csvHeader array
    # My csv will not have the "LastInspected" and "DateReported" cols. 
    # Will drop "LastInspected" but will keep "DateReported" as we will break it down into three cols for my csv file: "Date,Time,Hour" and then will drop it at the end
    jsonDF = jsonDF.drop(columns=["LastInspected"])                                                                 # Dropping this col fom the jsonDF                         
    csvHeader = list(jsonDF.drop(columns=["DateReported"]).columns.values)                                          # (this change will be replced is csv has header) Title: "DateReported" Will be replaced by "Date,Time,Hour" So will now 
    csvHeader.extend(replaceColWith)                                                                                # (this change will be replced is csv has header) Title: Adding the "Date,Time,Hour" to the title  
    try:
        with open(csvFile, 'r') as csvfile:                                                                             # Open the csv File so we can read it
            csvTable = [row for row in csv.DictReader(csvfile)]
            if len(csvTable) == 0:                                                                                      # a) csv is empty so add my header: [TicketNumber,Latitude,Longitude,Zip,ClassificationTyp,Date,Time,Hour
                with open(csvFile, 'w', newline='') as outf:
                    print("     Added Header: "+str(csvHeader))
                    writer = csv.writer(outf)
                    writer.writerow(csvHeader)
            else:
                csvHeader=list(pd.read_csv(csvFile).columns)                                                            # b) Since the csv already had data, it means i will append new data to it so just use the header of that csv file.    
                # print("     csv had data so copying the header")
    except Exception as e:
        csvReadCount = csvReadCount + 1
        if csvReadCount == 11:
            print("        Tried to read the csv file 11 times and failed, try next iteration")
            return
        print("     ...Couldnt read file so will re-run function...")
        print("    Error Code: "+str(e))
        scheduler.resume() #****resuming the job
        return WebscraperJsonToCSV()
        return
    csvReadCount = 0

    # 3) FIND THE NEW TICKETS 
    csvDF = pd.read_csv(csvFile)                                                                                    # Reading the list of tickets i current have on file and making a dataframe to read them
    mergedDF = jsonDF.merge(csvDF.drop_duplicates(), on=['TicketNumber'], how='left', indicator=True)               # Will take all the keys of jsonDF. Will merge with keys of right DF (wont display) and will keep only the merged keys 
    newTicketsArray = list(mergedDF.loc[mergedDF['_merge']=="left_only", "TicketNumber"])                           # This array holds all the tickets i dont have in my file
    newTicketDF = pd.DataFrame(columns=csvHeader)                                                                   # Making empty dataframe that has the columns of my csv file. This will be the df that will be modified and pushed to my csv
    if len(newTicketsArray) == 0:                                                                                   # No new Tickets, can end this iteration
        scheduler.resume() #****resuming the job
        return
    for row in range(0,len(newTicketsArray)):                                                                       # Going through the array of new ticket number and adding only their rows to th new data frame
        print("     "+newTicketsArray[row] + " not in set so adding it-----")
        newTicketDF = newTicketDF.append(jsonDF[jsonDF.TicketNumber == newTicketsArray[row]], sort=False, ignore_index=True)

    # 4 &) TURN THE MICROSOFT DATE IN "DateReported" INTO STANDARD FORMAT AND SEPERATE INTO "Date", "Time", "Hour" COLUMNS AND THEN DROP COLUMN "DateReported" :
    # 5) WILL USE THE CENSUS BUREAU API TO GET CENSUS DATA BASED ON EACH TICKET'S LONGITUDE AND LATITUDE DATA:             
    returnCols = [ "CensusTract_2010", "CensusBlock_2010", "CountyName_2010", "GEOID_2010", "CensusTract_2010_ID", "CensusTract_2010_NAME", "CensusBlock_2010_ID", "CensusBlock_2010_NAME"]  
    for row in range(0, len(newTicketDF)):                                                                          # Replacing DateReported with Date, Time, Hour columns
        print("     Getting Census data...")
        returnArray = getCensusTract(float(newTicketDF.loc[row]["Longitude"].item()), float(newTicketDF.loc[row]["Latitude"].item()))   # Returns: TractBASENAME, BlockBASENAME, CountyName, Geoid, TractID, TrackID Name, BlockID, Block Name] from Census Beru's API
        if returnArray[0] == 'error':                                                                                # if there is an error, stop this ticket from being read
            continue
        dateTimeHr = turnToDateTimeHr(str(newTicketDF["DateReported"][row]))                                        # Takes the microsoft date and returns: ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Date")] = dateTimeHr[0]                                  # Adding the Date, Time, Hour values to the appropriate cells
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Time")] = dateTimeHr[1]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Hour")] = dateTimeHr[2]
        if len(returnArray) == len(returnCols):
            for colToWrite in range(0, len(returnArray)):
                newTicketDF.at[row, returnCols[colToWrite]] = returnArray[colToWrite]
    newTicketDF = newTicketDF.drop(columns=["DateReported"])                                                        # Finally dropping the "DateReported" column    
    
    # 6) WRITE TO CSV FILE:
    print("     .....Appending new Gas Leak reports to file...")
    with open(csvFile,'a') as outCSV:                                                                               # Turning the DF into csv and appending the new data to the file
       outCSV.write(newTicketDF.to_csv(header=False, index=False))
    
    # 7) WRITING NEW HOURLY FILE BASED ON GAS LEAK HISTORY FILE AND PUSHING TO GH
    turnTickeyHistory_toHourlyReport()
    turnTickeyHistory_toMonthlyReport()
    git_push()
    scheduler.resume() #****resuming the job

# 8) RESCAN FOR TICKETS every x time using sceduler
scheduler = BlockingScheduler()
scheduler.add_job(WebscraperJsonToCSV, 'interval', minutes=30) # need to give enough time to go the entire process
scheduler.start()


# Notes: Turning the Gas Leak Report data into hourly reports...) process took forever, need to make it do it faster
