# 1) (Need to know all the tickets we got atm) read from the csv file's first column if it exists and add it to the dictionary 
# 2) read from a json file
# 3) put the ticket numbers into a dictionary if it doesnt exist
# 4) print that object into the csv file



import json
import csv
with open("test.json") as file:
    data_json = json.load(file)

# with open("test.csv", "w") as file:
#     data_csv = csv.writer(file)
#     for item in csv_file:
#         fields = list(item['fields'].values())
#         csv_file.writerow([item['pk'], item['model']] + fields)












