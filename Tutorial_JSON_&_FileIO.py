import json
import csv


############################################## 1) WRITE/APPEND to End of File ################################
# Step 1: Make a dictionary which will be the json file
data = {}
# Step 2: Json element
data['key1'] = 'value'
# Step 3: Json array object
data['aKey'] = []
data['aKey'].append({
    'property1': 'value1',
    'property2': 'value2'
})
data['aKey'].append({
    'property3': 'value3',
    'property4': 'value4'
})
# Step 4: append the json file (the dictionary) to the end of a file. 
# with open('test.json','a') as outf:
#     a = json.dumps(data, sort_keys=True, indent=4)                        # turns the dict() into a string. dict() is the same format as JSON. indent=4 to make it look good
#     outf.write(a)                                                         # append to end of list
############################################## 2) READ FROM JSON FILE #######################################
#For JSON Data: [{},{},{}] multiple JSON objects in one JSOn array
import pandas as pd
elem = [the keys inside every JSOn object {} ]
jsonDict = pd.read_json('test.json', orient='records')
for row in range(0, len(jsonDict)):             # go thru each row/JSON object
    s = ""
    for col in range(0, len(elems)):   # go through each column/JSON Object elements
        s+=str(jsonDict[elems[col]][row])+" "
    print(s)

# Older method:
with open('test.json',"r") as readf:
    dataj = json.load(readf)
print(dataj["key1"])

############################################## 3) CSV ###############################
import pandas as pd
csvData = pd.read_csv(csvFile)                           # Reading the CSV w Pandas: csvData[colStr][rowNumber]

with open('test.csv', 'r') as csvfile:                   # OLD MAthod Reading
    csv_empty = [row for row in csv.DictReader(csvfile)] # see if csv empty

with open('test.csv', 'w', newline='') as outf:          # Write this string s on the csv
    writer = csv.writer(outf)
    writer.writerow(s)
with open('test.csv','a') as out:                        # Asppend this string s on a new line
    out.write(s)

############################################# 4) Writing to txt #####################################
outf = open("file.txt","w+")
outf.write("This is line %d\r\n" % (i+1))








###################################################### JSOn to CSV older methods ###############################
########################## pandas:
# import pandas as pd
# df = pd.read_json('test.json')
# df.to_csv("test.csv")  #need to use two csv 
# df.to_csv("test.csv") 
######################### one step:
#pd.read_json('test.json').drop(columns=['LastInspected']).to_csv("test.csv", mode='a', header=False) #append to csv


################## older:
# jsonFileName = "test.json"
# csvHeader = ["key1", "property1", "property2","property3","property4"]
# with open(jsonFileName) as readf:
#     dataStrj = json.loads(readf.read())
# outf = csv.writer(open("test.csv","w", newline='')) #python2: "wb+". python3: "w", newline=''
# # Write the CSV header. write the keynames (if its a json obj, include only the inside keys)
# outf.writerow(csvHeader)    
# for d in dataStrj:
#     outf.writerow([
#         dataStrj['key1'],
#     ])
################### older:
# jsonFileName = "test.json"
# csvHeader = ["Ticket Number","Longitude","Latitude","Zipcode","Classification","Date Reported"]
# outf = csv.writer(open("test.csv","w", newline='')) #python2: "wb+". python3: "w", newline=''
# # Write the CSV header. write the keynames (if its a json obj, include only the inside keys)
# outf.writerow(csvHeader)    
# with open(jsonFileName) as readf:
#     dataStrj = json.loads(readf.read())
# for d in dataStrj:
#     outf.writerow([
#         dataStrj['Ticket Number']
#     ])











############################################## 3) CSV Read ###################################################
#with open('test.csv') as csvf:






