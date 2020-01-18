# Scraper v3: Will scrape data, add the Census data columns and then make a new csv
# Part 1 (section 1 to 4, 6): Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use
    # In the ConEdison Gas Leak Report Map, each report in the map represents a gas leak report. Each report has these seven keys: TicketNumber, Latitude, Longitude, Zipcode, Classification Type, Date Reported, Last Inspected.
    # a) We need to constantly add new repots to out list so what tickets do we currently have? read the ticket col of the "csvConEdFile" and add the tickets to "ticketSet"
    # b) Scrape the JSON html response and using pandas to put the contents into a dataframe called "jsonDF"
    # c) See if there is a new report: Loop through each JSON obbject in "jsonDF" and compare it to the reports are already exists in "ticketSet"
    # d) If there is a new report, add append the keys of that report into "csvConEdFile", "ticketListFile" and push the latest changes to github
# Part 2 (section 5):  Will edit the csv to have new columns for the Census Tract, Census Block, County Name and the hour only
    # Will use the census bureau api to get census data from the lat and lon coords using this url request:  https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x=LONGITUDE&y=LATITUDE&benchmark=Public_AR_Current&vintage=Current_Current&format=json
# Part 3: Will create a new csv that lists the reports per census tract per hour for that day. Headers: Date, Hour, Census Tract, Number of Reports

import json
import csv
import pandas as pd                                                                     # to read csv file and store conent into a data frame. To turn json response string into a dataframe
import datetime,re                                                                      # to turn Microsoft JSON date /Date()/ to normal date
import requests                                                                         # Getting html data
from bs4 import BeautifulSoup                                                           # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler                           # Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                                                                    # (GitPython) To push changes to gh


# SETTING UP GLOBAL VARIABLES: need to change the first eight variables below
csvFile = "GasHistory_ConEdisonTracts.csv"                                         # add new tickets to the end of the csv file
jsonFile = "SOME_JSON_FILE_WITH_SAME_KEYS.json"                                         # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&'              # Url to scrape JSOn data from
dropCol = True                                                                          # If you want to drop a column, specify which ones in step 2 in WebscraperJsonToCSV()
replaceColWith = ["Date", "Time", "Hour", "CensusTract", "CensusBlock", "CountyName" ]  # Replacing column DateReported with these "Date", "Time", "Hour and Made 3 more cols for Part 2 Census data

PATH_OF_GIT_REPO = r'/home/pi/repositories/gh/GasLeakProject'                           # the path to the .git file (.git location on my raspberry pi)
#PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject'                       # the path to the .git file (.git location on my Laptop)
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'                                   # the commmit message when it is pushed
scrapingCount = 0                                                                       # Just counting how many times i have scraped the website while this was running

# GIT PUSH FUNCTION: Setting up function to automatically push changes to github when there is a new ticket so that I can have access to the latest chnages
def git_push():
    repo = Repo(PATH_OF_GIT_REPO)
    try:
        repo.remotes.origin.pull()                                                      # try pulling new changes from the github repo (if there are any) so i can push changes
    except:
        print("Couldnt pull from repo")
    repo.git.add(update=True)
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    try:
        origin.push()                                                                   # try pushing the changes to github
        print("******** PUSHED TO GITHUB for Run " + str(scrapingCount)+"********")
    except:
        print('Some error occured while pushing the code')  


# FUNCTION TO TURN MICROSOFT JSON DATE TO mm/dd/yyyy AND TIME: returns ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
def turnToDateTimeHr(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    dateRaw = datetime.datetime.fromtimestamp(int(TimestampUtc))
    dateFormatted = str(dateRaw.strftime('%m/%d/20%y %I:%M %p'))                        # The datetime is of form: "mm/dd/tt hh:mm AM/PM"
    dateTimeSplit = dateFormatted.split(" ")                                            # ["mm/dd/yyyy", "hh:mm", "AM/PM"]
    date = dateTimeSplit[0]                                                             # Isolated the date string: "mm/dd/yyyy"
    time = dateTimeSplit[1] + " " + dateTimeSplit[2]                                    # Isolated the time string: "hh:mm AM/PM"
    hour = time.split(" ")[0].split(":")[0] + " " + dateTimeSplit[2]                    # Isolated the hour string: "hh AM/PM"   (will need for part 2)
    dateTimeHr = [date, time, hour]                                                     # ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
    return (dateTimeHr)                                                                

# PART 2 FUNCTION: Get [CensusTrack, CensusBlock, CountyName] from Longitude and Latitude coordintes using the Census Beru's API which returns a JSON file 
def getCensusTract(longitude, latitude,retryRun=0):                                     # returns an array [censusTract, CensusBlock, CountyName]
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates?x={0}&y={1}&benchmark=Public_AR_Current&vintage=Current_Current&format=json".format(longitude,latitude)
    if retryRun == 11:                                                                  # Failed to get json data 11 times with this longitude and latitude so need to skip this one
        print("*****Failed 11 times to get geodata so will print insert 'error'*****")
        return [str("error"), str("error"), str("error")]
    try:
        response = requests.get(url)
        dataJSON = response.json()
        data = dataJSON["result"]
        track = data["geographies"]["Census Tracts"][0]["BASENAME"]
        block = data["geographies"]["2010 Census Blocks"][0]["BLOCK"]
        county = data["geographies"]["Counties"][0]["NAME"] 
        return [str(track), str(block), str(county)]
    except:
        retryRun+=1
        print("Error on longitude, latitude: "+str(longitude)+","+str(latitude) + ".....retrying... "+str(retryRun))
        return getCensusTract(longitude, latitude,retryRun)                             # *****need to return the recursive function


# THE SCHEDULER WILL RUN THIS MAIN FUNCTION EVER X SECONDS/MINUTES/HOURS
def WebscraperJsonToCSV():  
    # Set up the web scraping iteration counter for debugging purposes
    global scrapingCount                                                                # Indicate that im using the global value
    scrapingCount = scrapingCount + 1 

    # 1) GET JSON DATA: Webscrape the html response which is usually just the JSON data from the url and add to the JSON Dataframe: 
    # jsonDF = pd.read_json(jsonFile, orient='records')                                # If im getting data from json file, comment out the rest of this section. form: jsonDF[keys[i]/colStr(report keys)][j/rowsnumber(reports)]
    try:
        res = requests.get(url)
        html_data = res.content                                                         # Getting the HTML JSON data from the url 
        soup = BeautifulSoup(html_data, 'html.parser')                                  # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
        text = soup.find_all(text=True)                                                 # Getting all the text thats in the soup
    except:
        print("Couldnt get the json data so will re-run function. This is Run "+ str(scrapingCount))
        return WebscraperJsonToCSV()
    jsonStr = ''                                                                    # turning text to string from so i can use pandas to turn it to a dataframe
    for t in text:
        jsonStr += '{} '.format(t)
    jsonDF = pd.read_json(jsonStr, orient='records')                              # Turning the json string to a pandas dataframe
    

    # 2) If the csv is empty, print the header. Else get the header and that is what we will work with. Im also droping columns from json DF and adding new col titles to csvHeader array
    # My csv will not have the "LastInspected" col. Will also break down "DateReported" into three cols for my csv file: "Date,Time,Hour"
    jsonDF = jsonDF.drop(columns=["LastInspected"])                                     # Dropping this col fom the jsonDF                         
    csvHeader = list(jsonDF.drop(columns=["DateReported"]).columns.values)              # (this change will be replced is csv has header) Title: "DateReported" Will be replaced by "Date,Time,Hour" So will now 
    csvHeader.extend(replaceColWith)                                                    # (this change will be replced is csv has header) Title: Adding the "Date,Time,Hour" to the title
    
    with open(csvFile, 'r') as csvfile:                                                         # Open the csv File so we can read it
        csvTable = [row for row in csv.DictReader(csvfile)]
        if len(csvTable) == 0:                                                                 # csv is empty so add my header: [TicketNumber,Latitude,Longitude,Zip,ClassificationTyp,Date,Time,Hour
            with open(csvFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)
                print("Added Header")
        else:
            csvHeader=list(pd.read_csv(csvFile).columns)                                # Since the csv already had data, just use the header of that csv file
            

    # 3) FIND THE NEW TICKETS 
    csvDF = pd.read_csv(csvFile)                                                        # Reading the list of tickets i current have on file and making a dataframe to read them
    mergedDF = jsonDF.merge(csvDF.drop_duplicates(), on=['TicketNumber'], how='left', indicator=True) # Will take all the keys of jsonDF. Will merge with keys of right DF (wont display) and will keep only the merged keys 
    newTicketsArray = list(mergedDF.loc[mergedDF['_merge']=="left_only", "TicketNumber"])   # This array holds all the tickets i dont have in my file
    newTicketDF = pd.DataFrame(columns=csvHeader)                                       # Making empty dataframe that has the columns of my csv file. This will be the df that will be modified and pushed to my csv

    if len(newTicketsArray) == 0:                                                           # No new Tickets, can end this iteration
        return


    for row in range(0,len(newTicketsArray)):
        # print(newTicketsArray[row] + " not in set so adding it-----")
        newTicketDF = newTicketDF.append(jsonDF[jsonDF.TicketNumber == newTicketsArray[row]], sort=False, ignore_index=True)

    # 4 &) TURN THE MICROSOFT DATE IN "DateReported" INTO STANDARD FORMAT AND SEPERATE INTO "Date", "Time", "Hour" COLUMNS 
    # 5) WILL USE THE CENSUS BUREAU API TO GET CENSUS DATA BASED ON EACH TICKET'S LONGITUDE AND LATITUDE DATA:             
    for row in range(0, len(newTicketDF)):                                      # Replacing DateReported with Date, Time, Hour columns
        dateTimeHr = turnToDateTimeHr(str(newTicketDF["DateReported"][row]))    # Takes the microsoft date and returns: ["mm/dd/yyyy", "hh:mm AM/PM", "hh AM/PM"]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Date")] = dateTimeHr[0]  # Adding the Date, Time, Hour values to the appropriate cells
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Time")] = dateTimeHr[1]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("Hour")] = dateTimeHr[2]
 
        returnArray = getCensusTract(float(newTicketDF.loc[row]["Longitude"].item()), float(newTicketDF.loc[row]["Latitude"].item()))   # returns: [CensusTrack, CensusBlock, CountyName] from Census Beru's API
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("CensusTract")] = returnArray[0] # Adding the CensusTrack, CensusBlock, CountyName values to the appropriate cells
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("CensusBlock")] = returnArray[1]
        newTicketDF.iloc[row, newTicketDF.columns.get_loc("CountyName")] =  returnArray[2]
    
    newTicketDF = newTicketDF.drop(columns=["DateReported"])                         # Finally dropping the "DateReported" column    
    newTicketDF.to_csv(csvFile, mode='a', header=False, index=False)                 # Print to csv file
    file_data = open(csvFile, 'rb').read()
    open(csvFile, 'wb').write(file_data[:-2])

    # 6) Push to Github if we have a new ticket
    git_push()
    print("Run Done " + str(scrapingCount) + "       Reports Scraped: "+str(len(jsonDict)))

WebscraperJsonToCSV()
