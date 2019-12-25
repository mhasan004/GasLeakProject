# Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use

# 1) What tickets do we have? read the ticket col of csv of ticket txt file and add tickets to ticketList.txt
# 2) jsonDict = contents of json file
# 3) Loop through the ticketNumber dictionary key and compare it to tickets in the ticketList.txt
    # 4) if the ticket exists, ignore it. If it dont exist 
        #a) add the ticket to the ticketList.txt and .csv files for storage and also add new ticket to the tickeSet

import json
import csv
import pandas as pd                 # to read the json and csv data and put into dictionary form
import datetime                     # to turn Microsoft JSON date /Date()/ to normal date
import re                           # to turn Microsoft JSON date /Date()/ to normal date
import requests                     # Getting html data
from bs4 import BeautifulSoup       # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler #Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                # To push chnages to gh


# Setting up variables:
jsonFile = "ConEdGasLeakList_ManualRecords_UNION.json"          # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&' # Url to scrape JSOn data from
csvFile = "UNION.csv"                                           # add new tickets to the end of the csv file
ticketListFile = "ticketList.txt"                               # add to end (just for me to see what i got)
ticketSet = set()                                               # need to add what i got in the csv atm
jsonDict  = []                                                  # json file to dict: #jsonDict["TicketNumber/Long/lat/etc"][int index of the dot]) 
scrapingCount = 0                                               # Just counting how many times i have scraped the website while this was running
properties= [                                                   # Need this to acces the dot properties
    "TicketNumber",
    "Latitude",
    "Longitude",
    "Zip",
    "ClassificationType",
    "DateReported",
    "LastInspected"
]
# Setting up method to automatically push changes to git hub so i can access the new tickets
PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject'  # the path to the .git file
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'
def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

# Function to turn Microsoft JSON date to mm/dd/yy and time:
def turnToDatetime(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    date = datetime.datetime.fromtimestamp(int(TimestampUtc))
    return str(date.strftime('%m/%d/20%y %I:%M %p'))            # mm/dd/yyyy time am/pm


# The sceduler will run this main funtion ever x seconds/minutes/hours
def WebscraperJsonToCSV():                                  
    # 1) If the csv is empty, print the header
    with open(csvFile, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            csvHeader = ["TicketNumber","Longitude","Latitude","Zipcode","Classification","DateReported"]
            with open(csvFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)

    # 2) Get JSON data from a JSON file and add to the JSON Dictionary: 
        # jsonDict = pd.read_json(jsonFile, orient='records')           # ***jsonDict[properties[i]/colStr(dot properties)][j/rowsnumber(dots)]

    # 2) Webscrape JSON data from the url and add to the JSON Dictionary: 
    res = requests.get(url)
    html_data = res.content                                             # Getting the HTML JSOn data 
    soup = BeautifulSoup(html_data, 'html.parser')                      # the HTML data to parse
    text = soup.find_all(text=True)

    jsonStr = ''                                                        # turning text to string from so i can use pandas to turn it to dictionary
    for t in text:
        jsonStr += '{} '.format(t)
    jsonDict = pd.read_json(jsonStr, orient='records')                  # Turning the json string to a dictionary

    # 3) Read the csv file and add "TicketNumbers" to the "ticketSet" and print ticketNumber to ticketList.txt" for storage: 
    csvData = pd.read_csv(csvFile)                                      # ***csvData[colStr][rowNumber]
    outTXT = open(ticketListFile,"w+")                                  # Settign up to write to txt file
    for row in range(0,len(csvData)):
        ticketSet.add(str(csvData["TicketNumber"][row]))    
        outTXT.write(str(csvData["TicketNumber"][row])+"\n")

    # 4) CHECK IF NEW TICKET: See if the tickets in "jsonDict" are in "ticketDict". If we have have it, add to "ticketDic", and .txt and .csv file for stoage. If we have it, skip this row since we have this info already. 
    for row in range(0, len(jsonDict)):
        if jsonDict["TicketNumber"][row] not in ticketSet:              # If we DONT have this ticket add it
            print(str(jsonDict["TicketNumber"][row])+ " not in set so adding it")
            ticketSet.add(jsonDict["TicketNumber"][row])
            outTXT.write(jsonDict["TicketNumber"][row]+"\n")            # add new ticket to txt file  
            with open(csvFile,'a') as outCSV:                           # Write the new Ticket object to csv file
                s=""
                for col in range(0, len(properties)-1):                 # go through each column/dot property
                    if properties[col] == "DateReported":               # Need to change the Microsoft time to mm/dd/yyyy
                        s+=turnToDatetime(str(jsonDict[properties[col]][row]))
                    else: 
                        s+=str(jsonDict[properties[col]][row])
                    if col != len(properties)-2:
                        s+=',' 
                s+="\n"
                outCSV.write(s)                                         # add new ticket obj to csv file  
        git_push()

    # 5) print the web scraping run that was done for debugging purposes
    global scrapingCount                                                # Indicate that im using the global value
    scrapingCount = scrapingCount + 1 
    print("Run Done " + str(scrapingCount))

# Running the function every x seconds/minutes/hours
scheduler = BlockingScheduler()
scheduler.add_job(WebscraperJsonToCSV, 'interval', seconds=30)
scheduler.start()


       






