# Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use
# File with web scraper

# 1) What tickets do we have? read the ticket col of csv of ticket txt file and add tickets to ticketList.txt
# 2) jsonDict = contents of json file
# 3) Loop through the ticketNumber dictionary key and compare it to tickets in the ticketList.txt
    # 4) if the ticket exists, ignore it. If it dont exist 
        #a) add the ticket to the ticketList.txt and .csv files for storage and also add new ticket to the tickeSet

import json
import csv
import pandas as pd     # to read the json and csv data and put into dictionary form
import datetime         # to turn Microsoft JSON date /Date()/ to normal date
import re               # to turn Microsoft JSON date /Date()/ to normal date
import requests                     # Getting html data
from bs4 import BeautifulSoup       # Parse the HTML data

# Function to turn Microsoft JSON date to mm/dd/yy and time:
def turnToDatetime(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    date = datetime.datetime.fromtimestamp(int(TimestampUtc))
    return str(date.strftime('%m/%d/20%y %I:%M %p')) # mm/dd/yyyy time am/pm

# Setting up variables:
jsonFile = "ConEdGasLeakList_ManualRecords_UNION.json"      # constantly reading from this file and adding new tickets to csv and txt files (will scrape from json web site)
csvFile = "UNION.csv"                                       # add new tickets to the end of the csv file
ticketListFile = "ticketList.txt"                           # add to end (just for me to see what i got)
ticketSet = set()                                           # need to add what i got in the csv atm
jsonDict  = []                                              # json file to dict: #jsonDict["TicketNumber/Long/lat/etc"][int index of the dot]) 
properties= [                                                     # Need this to acces the dot properties
    "TicketNumber",
    "Latitude",
    "Longitude",
    "Zip",
    "ClassificationType",
    "DateReported",
    "LastInspected"
]


# 1) If the csv is empty, print the header
with open(csvFile, 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        csvHeader = ["TicketNumber","Longitude","Latitude","Zipcode","Classification","DateReported"]
        with open(csvFile, 'w', newline='') as outf:
            writer = csv.writer(outf)
            writer.writerow(csvHeader)

# 2) Get JSON data from the JSON file and add to the JSON Dictionary: 
    # jsonDict = pd.read_json(jsonFile, orient='records')         # ***jsonDict[properties[i]/colStr(dot properties)][j/rowsnumber(dots)]

# 2) Webscrape JSON data from the url and add to the JSON Dictionary: 
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&'
res = requests.get(url)
html_data = res.content                                         # Getting the HTML JSOn data 
soup = BeautifulSoup(html_data, 'html.parser')                  # the HTML data to parse
text = soup.find_all(text=True)

jsonStr = ''                                                    # turning text to string from so i can use pandas to turn it to dictionary
for t in text:
	jsonStr += '{} '.format(t)

jsonDict = pd.read_json(jsonStr, orient='records')              # Turning the json string to a dictionary







# 3) Read the csv file and add "TicketNumbers" to the "ticketSet" and print ticketNumber to ticketList.txt" for storage: 
csvData = pd.read_csv(csvFile)                              # ***csvData[colStr][rowNumber]
outTXT = open(ticketListFile,"w+")                          # Settign up to write to txt file
for row in range(0,len(csvData)):
    ticketSet.add(str(csvData["TicketNumber"][row]))    
    outTXT.write(str(csvData["TicketNumber"][row])+"\n")


# 4) See if the ticket in "jsonDict" is in "ticketDict". If dont got add to "ticketDic", and .txt and .csv file for stoage. If got, skip this row since we have this info already. 
for row in range(0, len(jsonDict)):
    if jsonDict["TicketNumber"][row] not in ticketSet:      # If we DONT have this ticket add it
        print(str(jsonDict["TicketNumber"][row])+ " not in set so adding it")
        ticketSet.add(jsonDict["TicketNumber"][row])
        outTXT.write(jsonDict["TicketNumber"][row]+"\n")    # add new ticket to txt file  
        with open(csvFile,'a') as outCSV:                   # Write the new Ticket object to csv file
            s=""
            for col in range(0, len(properties)-1):               # go through each column/dot property
                if properties[col] == "DateReported":             # Need to change the Microsoft time to mm/dd/yyyy
                    s+=turnToDatetime(str(jsonDict[properties[col]][row]))
                else: 
                    s+=str(jsonDict[properties[col]][row])
                if col != len(properties)-2:
                    s+=',' 
            s+="\n"
            outCSV.write(s)                                 # add new ticket obj to csv file  

# 5) Commit chnages to gh
       






