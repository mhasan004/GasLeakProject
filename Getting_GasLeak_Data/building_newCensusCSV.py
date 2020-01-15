# PART 3: now making new csv that is based on time
import pandas as pd                                                                     # To read and write csv files

csvInFile  = "GasHistory_ConEdisonTracts.csv"
csvOutFile = "reportsPerCensusTract.csv"


df = pd.read_csv(csvInFile)  
dateArray = []
timeArray = []                                                        
for row in range(0,len(df)):
    dateTime = df["DateReported"][row].split(' ')                       # [mm/dd/yyyy, time, am/pm]
    dateArray.append(dateTime[0])
    timeArray.append(dateTime[1]+" "+dateTime[2])
