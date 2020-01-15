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
csvData = pd.read_csv(csvFile)                           # READING the CSV w Pandas df (panas df makes stuff easier): csvData[colStr][rowNumber]

with open('test.csv', 'r') as csvfile:                   # OLD METHOD Reading
    csv_empty = [row for row in csv.DictReader(csvfile)] # see if csv empty

with open('test.csv', 'w', newline='') as outCSV:        # WRITING: clear the csv and write this string s on the csv
    writer = csv.writer(outCSV)
    writer.writerow(s)

with open('test.csv','a') as outCSV:                     # WRITING: Append this string s on a new line
    outCSV.write(s)

# add new col to csv:
df = pd.read_csv("csvFile.csv")                         # WRITING NEW COL: read the csv file and store to df
color=['red','green', 'blue']                           # 1) adding these data to each row for this col
df['colors'] = color                                    # 2) adding a new col named "colors" and add the row vals in
df.to_csv("csvFile.csv")                                # 3) back to csv

############################################# Pandas dataframe access ############
# ACCESSING ELEMENTS USING loc, iloc, ix:
    df.iloc[0][1]                               # (can also use loc) access te 0th row, 1st col element
    df.loc["row1", "row2"]["col1,col2"]         # by name of cols
    df.iloc[1]["col1"]                          # accessing the index 1 elem of col "col1"
    df.loc[0,:]                                 # the 0th row
    #*** these will return numpy datatype to chnage to python add .item(). example below
# SPECIFICS:
df["column in focusing on"][rowNumber]          # accesing an elemen of certain col
df["col1", "col2"]                              # prints these columns only

# FILTERING: only prints entries where the col "sex" is "M"
    df.sex == "M"                              # 1) BOOLEAN: prints the zipcode col but has only True or False values        
    df[df.sex == "M" ]                         # 2 only prints the entries where "sex" is "M"                         

# TYPE numpy.float64 to python float
    df.loc[1]["col1"].item() # if this returns numpy.float64, it is now float

# PRINT COLUMN NAMES:
    for col in df.columns:                    # method 1:
        print(col)
    print(list(df.columns))                   # method 2
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






