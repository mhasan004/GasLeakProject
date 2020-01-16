# PART 3: now making new csv that is based on time
# 1) df = get the csv data.
# 2) dateDF = loop throught the "Date" column and and make a new data frame for entries that has same Date
# 3) hourlyDF = for each dateDF, loop through the "Hour" column and make a new data frame for entries that has same Hour 
# 4) tractDF  = for each hourlyDF, loop through the "Census Tract" column and make a new data frame for entries that has same Hour 
import pandas as pd                                                                     # To read and write csv files

csvInFile  = "GasHistory_ConEdisonTractsTest.csv"
csvOutFile = "reportsPerCensusTract.csv"
# censusTractIndex = 6    #Need to add these indexes because when i iterate through the rows, need to use these to find appropiate values
# dateIndex = 9
# hourIndex= 11


dateCol = []
hourCol = []
censusTractCol = []
countCol = []
indexToSkip = []

df = pd.read_csv(csvInFile) 
print(len(df)) 
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

                        print(
                            "Date: " + str(tractDF.iloc[0]["Date"]) 
                            + "     Hour: "        + str(tractDF.iloc[0]["Hour"])
                            + "     CensusTract: " + str(tractDF.iloc[0]["CensusTract"] )
                            + "     Count: "       + str(len(tractDF))
                        )
                        









# tempdf = df[df.Date == "12/17/2019"]                                             # making new df = targeted rows
# print("need to del these and add to skip array: "+ str(df.index[df['Date'] == "12/18/2019"].tolist()))
# indexToSkip.extend(df.index[df['Date'] == "12/18/2019"].tolist())                # adding the index of those targeted rows so can skip them since we already added thme to csv
# print(str(indexToSkip)+"\n--------------------")   


# rowsToDel = df.index[df['Date'] == "12/18/2019"].tolist()  # List the index of target rows
# df= df.drop(df.index[rowsToDel])                       # deleting target rows

