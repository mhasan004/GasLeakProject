# 1) What tickets do we have? read the ticket col of csv of ticket txt file and add tickets to ticketDictionary
# 2) anotherDict = contents of json file
# 3) Loop through the ticketNumber dictionary key and compare it to tickets in the ticketDictionary
    # 4) if the ticket exists, ignore it. If it dont exist 
        #a) add the ticket to the dictionay.txt file and the tickeDictionary and push to end of csv
        #b)
import json
import csv
import pandas as pd     # to read the json data
import datetime         # to turn Microsoft JSON date /Date()/ to normal date
import re               # to turn Microsoft JSON date /Date()/ to normal date
def turnToDatetime(microsoftDate):          # Function to turn Microsoft JSOn date to mm/dd/yy and time
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    date = datetime.datetime.fromtimestamp(int(TimestampUtc))
    return str(date.strftime('%m/%d/20%y %I:%M %p')) # mm/dd/yyyy time am/pm


csvFileName = "test.csv"                    # add to the end
jsonFileName = "test.json"                  # constant read (json web site)
dictionaryFileName= "ticketDictionary.txt"  # add to end (just for me to see what i got)
ticketSet = set()                           # need to add what i got in the csv atm
jsonDict  = []                              # json file to dict: #jsonDict["TicketNumber/Long/lat/etc"][int index of the dot]) 
dotp= [                                     # Need this to acces the dot properties
    "TicketNumber",
    "Latitude",
    "Longitude",
    "Zip",
    "ClassificationType",
    "DateReported",
    "LastInspected"
]




# 1) If the csv is empty, print the header
with open('test.csv', 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        csvHeader = ["TicketNumber","Longitude","Latitude","Zipcode","Classification","DateReported"]
        with open('test.csv', 'w', newline='') as outf:
            writer = csv.writer(outf)
            writer.writerow(csvHeader)

# 2) Add the new JSON data to the Json Dictionary: jsonDict[dotp[i]/columns(dot properties)][j/rows(dots)]
jsonDict = pd.read_json('test.json', orient='records')
    # for row in range(0, len(jsonDict)):         # go thru each row/dot
    #     s = ""
    #     for col in range(0, len(dotp)):         # go through each column/dot property
    #         s+=str(jsonDict[dotp[col]][row])+" "
    #     print(s)

# 3) read the csv file and add ticket Nubers to the ticketSet



# 4) See if the ticket in "jsonDict" is in "ticketDict". If dont got add to "ticketDic", txt and csv. If got, skip this row since we have this info already. 
for dotN in range(0, len(jsonDict)):
    if jsonDict["TicketNumber"][dotN] not in ticketSet: # If we DONT have this ticket add it
        ticketSet.add(jsonDict["TicketNumber"][dotN])
        with open('test.csv','a') as out:
            s=""
            for col in range(0, len(dotp)-1):            # go through each column/dot property
                if dotp[col] == "DateReported":         # Need to change the Microsoft time to mm/dd/yyyy
                    s+=turnToDatetime(str(jsonDict[dotp[col]][dotN]))
                else: 
                    s+=str(jsonDict[dotp[col]][dotN])
                if col != len(dotp)-2:
                    s+=',' 
            s+="\n"
            out.write(s)



# Append the other stuff
# pd.read_json('test.json').drop(columns=['LastInspected']).to_csv("test.csv", mode='a', header=False) #append to csvuse ("test.csv", mode='a', header=False)










