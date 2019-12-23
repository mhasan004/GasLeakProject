import json
import csv

############################################## WRITE/APPEND to End of File ################################
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
# with open('test.json','a') as outfile:
#     a = json.dumps(data, sort_keys=True, indent=4)              # turns the dict() into a string. dict() is the same format as JSON. indent=4 to make it look good
#     outfile.write(a)                                            # append to end of list

############################################## READ FROM JSON FILE #######################################
with open('test.json',"r") as readf:
    data = json.load(readf)
print(data["key"])