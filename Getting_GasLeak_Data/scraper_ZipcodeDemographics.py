########## THIS IS A ONE TIME SCRAPER ###########
# Using the NYC Open Data API

import pandas as pd
from sodapy import Socrata
import csv
# A) SETTING UP VARS
USERNAME = "mhasan0047@gmail.com"
PASSWORD = "s0mePass212"
APP_TOKEN = "I2iI5wKFvjnajBahyxLb5IjBz"
csvFile = "DemographicHistory_NYVOpenData.csv"                                       # add new ticketreports to the end of the csv file

# B) GETTING DATA
client = Socrata("data.cityofnewyork.us",
    APP_TOKEN,
    username = USERNAME,
    password = PASSWORD, 
    timeout = 5
)

results = []
print("Filtering...")
results = client.get("kku6-nxdu")
# results = client.get("8m42-w767", select = "*", where = "incident_classification = 'Utility Emergency - Gas'", limit = 990000)
print("Done Filtering. Now to main proces...")

# C) Get all the key/properties of the JSON data and put it into a set so we can retrieve any value
resultKeys = []
for key in results[0]:
    resultKeys.append(str(key))

# D) Print data to csv
# 1) If the csv is empty, print the header
with open(csvFile, 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        with open(csvFile, 'w', newline='') as outf:
            writer = csv.writer(outf)
            writer.writerow(resultKeys)

# 2
print("Printing...")
for row in range(0,len(results)):
    with open(csvFile,'a') as outCSV:                           # Write the new Ticket object to csv file
        s = ""
        for key in results[row]:
            s+=results[row][key]+","
        s+="\n"
        outCSV.write(s)  
