#Using the NYC Open Data API
import pandas as pd
from sodapy import Socrata
import csv
# A) Getting JSON data from the API
USERNAME = "xchen008@citymail.cuny.edu"
PASSWORD = "Cpe2020."
APP_TOKEN = "JAl95Xdvrj7viLN3NEKF1vPEY"
Key_ID = "4e4eghj35p3ravbeff0yryp40"
client = Socrata("data.cityofnewyork.us",
                  APP_TOKEN,
                  username = USERNAME,
                  password = PASSWORD, timeout = 5)
results = []
print("Filtering...")
results = client.get("8m42-w767", select = "*", where = "incident_classification = 'Utility Emergency - Gas'", limit = 990000)
print("Done Filtering. Now to main proces...")

# B) Get all the key/properties of the JSON data and put it into a set so we can retrieve any value
resultKeys = []
for key in results[0]:
    resultKeys.append(str(key))

# C) Print data to csv
# 1) If the csv is empty, print the header
csvFile = "NYFD_GasHistory.csv"                                       # add new ticketreports to the end of the csv file
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
