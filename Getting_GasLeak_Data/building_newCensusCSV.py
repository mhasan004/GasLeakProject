# PART 3: now making new csv that is based on time
# 1) df = get the csv data.
# 2) dateDF = loop throught the "Date" column and and make a new data frame for entries that has same Date
# 3) hourlyDF = for each dateDF, loop through the "Hour" column and make a new data frame for entries that has same Hour 
# 4) tractDF  = for each hourlyDF, loop through the "Census Tract" column and make a new data frame for entries that has same Hour 
import pandas as pd                                                                     # To read and write csv files

csvInFile  = "GasHistory_ConEdisonTracts.csv"
csvOutFile = "reportsPerCensusTract.csv"

dateCol = []
hourCol = []
censusTractCol = []
countCol = []
indexToSkip = []

df = pd.read_csv(csvInFile) 
print(len(df)) 
s = ""
for row in range(0,len(df)):
    date = df.iloc[row]["Date"]
    if row not in indexToSkip:                                                                     # A) Do this Date if i didnt do so already: 
        dateDF = df[df.Date == date]                                                                    # 1) new df = target rows (which were recorded in the same date?)
        indexToSkip.extend(df.index[df["Date"] == date].tolist())                                       # 2) adding the index of those targeted rows so can skip them since we go down the entires

        hourToSkip = []
        for rowHour in range(0, len(dateDF)):
            hour = dateDF.iloc[rowHour]["Hour"]   
            if rowHour not in hourToSkip:                                                           # B) Do this Hour if i didnt do so already:                 
                hourlyDF = dateDF[dateDF.Hour == hour]                                                  # 1) new df = target rows (of those same date, which were recorded in the same hour?)                  
                hourToSkip.extend(dateDF.index[dateDF["Hour"] == hour].tolist())                        # 2) adding the index of those targeted rows so can skip when we go down the row for this date   
                
                tractToSkip = []
                for rowTract in range(0, len(hourlyDF)):                                    
                    tract = hourlyDF.iloc[rowTract]["CensusTract"]          
                    if rowTract not in tractToSkip:                                                 # C) Do this Census Tract if i didnt do so already: 
                        tractDF = hourlyDF[hourlyDF.CensusTract == tract]                               # 1) new df = target rows (of those same hours, which were recorded in the same census tract?)                  
                        tractToSkip.extend(hourlyDF.index[hourlyDF["CensusTract"] == tract].tolist())   # 2) adding the index of those targeted rows so can skip when we go down the row for this hour
                        s += tractDF.iloc[0]["Date"] + "," + str(tractDF.iloc[0]["Hour"]) + "," + str(tractDF.iloc[0]["CensusTract"]) + "," + str(len(tractDF)) + "\n"
                        # print("###############################################################################")
                        # print(tractDF)
                        # print(
                        #     "Date: " + str(tractDF.iloc[0]["Date"]) 
                        #     + "     Hour: "        + str(tractDF.iloc[0]["Hour"])
                        #     + "     CensusTract: " + str(tractDF.iloc[0]["CensusTract"] )
                        #     + "     Count: "       + str(len(tractDF))
                        # )
                        # print("###############################################################################")
print(s)
with open(csvOutFile,'a') as outCSV:                           # Write the stuff to the csv file
    outCSV.write(s)   



