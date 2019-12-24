# 1) (Need to know all the tickets we got atm) read from the csv file's first column if it exists and add it to the dictionary 
# 2) read from a json file
# 3) put the ticket numbers into a dictionary if it doesnt exist
# 4) print that object into the csv file
import json
import csv
import pandas as pd
# df = pd.read_json('test.json')
# df.to_csv("test.csv")  #need to use two csv 
# df.to_csv("test.csv") 

csvFileName = "test.csv"
jsonFileName = "test.json"

# If the csv is empty, print the header
with open('test.csv', 'r') as csvfile:
    csv_dict = [row for row in csv.DictReader(csvfile)]
    if len(csv_dict) == 0:
        csvHeader = ["Ticket Number","Longitude","Latitude","Zipcode","Classification","Date Reported"]
        outf = csv.writer(open("test.csv","w", newline='')) 
        outf.writerow(csvHeader)  

# Append the other stuff
pd.read_json('test.json').drop(columns=['LastInspected']).to_csv("test.csv", mode='a', header=False) #append to csvuse ("test.csv", mode='a', header=False)










