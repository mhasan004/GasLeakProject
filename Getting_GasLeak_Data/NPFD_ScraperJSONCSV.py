#Using the NYC Open Data API
import pandas as pd
from sodapy import Socrata
USERNAME = "xchen008@citymail.cuny.edu"
PASSWORD = "Cpe2020."
APP_TOKEN = "JAl95Xdvrj7viLN3NEKF1vPEY"
Key_ID = "4e4eghj35p3ravbeff0yryp40"
client = Socrata("data.cityofnewyork.us",
                  APP_TOKEN,
                  username = USERNAME,
                  password = PASSWORD, timeout = 5)
results = []
results = client.get("8m42-w767", select = "*", 
                     where = "incident_classification = 'Utility Emergency - Gas'", limit = 990000)
# # erm2-nwe9 311 data
# # 8m42-w767 fire incident

# results_df = pd.DataFrame.from_records(results)
# #for i, j in results_df.iterrows(): //i is index, j is data
# #    print(j + "\n")

# print(len(results))

count = 0
for row in range(0,len(results)):
    s = ""
    if results[row]["incident_classification"] == "Utility Emergency - Gas":
        count+=1
        for key in results[row]:
            s+=results[row][key]+", "
    # print(s)
print(count)