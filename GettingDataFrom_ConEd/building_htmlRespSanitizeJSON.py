# Mahmudul Hasan. Script to scrape JSON Gas Leak Data points from ConEdison everyday and put them into a csv file for further use

# 1) What tickets do we have? read the ticket col of csv of ticket txt file and add tickets to ticketList.txt
# 2) jsonDict = contents of json file
# 3) Loop through the ticketNumber dictionary key and compare it to tickets in the ticketList.txt
    # 4) if the ticket exists, ignore it. If it dont exist 
        #a) add the ticket to the ticketList.txt and .csv files for storage and also add new ticket to the tickeSet

import json
import csv
import pandas as pd                 # to read the json and csv data and put into dictionary form
import datetime                     # to turn Microsoft JSON date /Date()/ to normal date
import re                           # to turn Microsoft JSON date /Date()/ to normal date
import requests                     # Getting html data
from bs4 import BeautifulSoup       # Parse the HTML data
from apscheduler.schedulers.blocking import BlockingScheduler #Sceduler. Will run a function every x seconds/minutes/hours
from git import Repo                # (GitPython) To push chnages to gh


# SETTING UP GLOBAL VARIABLES: need to change the first seven variables below
jsonFile = "ex.json"          # Normally the programm will be scrape JSOn data from a url but sometimes it might need to extract JSOn data from a file. See step 2)
url = 'https://apps.coned.com/gasleakmapweb/GasLeakMapWeb.aspx?ajax=true&' # Url to scrape JSOn data from
csvFile = "UNION.csv"                                           # add new tickets to the end of the csv file
ticketListFile = "ticketList.txt"                               # add to end (just for me to see what i got)
properties= [                                                   # The JSON dot properties
    "TicketNumber",
    "Latitude",
    "Longitude",
    "Zip",
    "ClassificationType",
    "DateReported",
    "LastInspected"
]
#PATH_OF_GIT_REPO = r'/home/pi/repositories/gh/GasLeakProject'  # the path to the .git file (.git location on my raspberry pi)
PATH_OF_GIT_REPO = r'/home/hasan/repositories/gh/GasLeakProject' # the path to the .git file (.git location on my Laptop)
COMMIT_MESSAGE = 'Automated Push - New Ticket Update'           # the commmit message when it is pushed
ticketSet = set()                                               # need to add what i got in the csv atm
jsonDict  = []                                                  # json file to dict: #jsonDict["TicketNumber/Long/lat/etc"][int index of the dot]) 
scrapingCount = 0                                               # Just counting how many times i have scraped the website while this was running

# GIT PUSH FUNCTION: Setting up function to automatically push changes to github when there is a new ticket so that I can have access to the latest chnages
def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        print("******** PUSHED TO GITHUB for Run " + str(scrapingCount)+"********")
    except:
        print('Some error occured while pushing the code')  
  

# Function to turn Microsoft JSON date to mm/dd/yy and time:
def turnToDatetime(microsoftDate):         
    TimestampUtc = str(microsoftDate)
    TimestampUtc = re.split('\(|\)', TimestampUtc)[1][:10]
    date = datetime.datetime.fromtimestamp(int(TimestampUtc))
    return str(date.strftime('%m/%d/20%y %I:%M %p'))                    # mm/dd/yyyy time am/pm


# The sceduler will run this main funtion ever x seconds/minutes/hours
def WebscraperJsonToCSV():    
    # Set up the web scraping iteration counter for debugging purposes
    global scrapingCount                                                # Indicate that im using the global value
    scrapingCount = scrapingCount + 1 
    isNewTicket = False

    # 1) If the csv is empty, print the header
    with open(csvFile, 'r') as csvfile:
        csv_dict = [row for row in csv.DictReader(csvfile)]
        if len(csv_dict) == 0:
            csvHeader = ["TicketNumber","Longitude","Latitude","Zipcode","Classification","DateReported"]
            with open(csvFile, 'w', newline='') as outf:
                writer = csv.writer(outf)
                writer.writerow(csvHeader)



    # 2) redoint the scraper
    # res = requests.get(url)
    # html_data = res.content                                             # Getting the HTML JSOn data 
    html_data = b'[
        {"TicketNumber":"ML19001225","Latitude":40.75402,"Longitude":-73.97419,"Zip":"10017","ClassificationType":"M","DateReported":"\/Date(1548123352000)\/","LastInspected":"\/Date(1548347559000)\/"},
        {"TicketNumber":"ML19003831","Latitude":40.77168,"Longitude":-73.97763,"Zip":"10023","ClassificationType":"M","DateReported":"\/Date(1551966025000)\/","LastInspected":"\/Date(1570796888000)\/"},
        {"TicketNumber":"ML19004663","Latitude":40.75472,"Longitude":-73.97591,"Zip":"10017","ClassificationType":"M","DateReported":"\/Date(1553211480000)\/","LastInspected":"\/Date(1555940700000)\/"},
        {"TicketNumber":"ML19005447","Latitude":40.80325,"Longitude":-73.96749,"Zip":"10025","ClassificationType":"M","DateReported":"\/Date(1554403835000)\/","LastInspected":"\/Date(1566270397000)\/"},
        {"TicketNumber":"ML19006608","Latitude":40.78175,"Longitude":-73.96026,"Zip":"10028","ClassificationType":"M","DateReported":"\/Date(1556374519000)\/","LastInspected":"\/Date(1577103600000)\/"}
        ] 
        html 


        Session state has created a session id, but cannot save it because the response was already flushed by the application. 


                body {font-family:"Verdana";font-weight:normal;font-size: .7em;color:black;} 
                p {font-family:"Verdana";font-weight:normal;color:black;margin-top: -5px}
                b {font-family:"Verdana";font-weight:bold;color:black;margin-top: -5px}
                H1 { font-family:"Verdana";font-weight:normal;font-size:18pt;color:red }
                H2 { font-family:"Verdana";font-weight:normal;font-size:14pt;color:maroon }
                pre {font-family:"Consolas","Lucida Console",Monospace;font-size:11pt;margin:0;padding:0.5em;line-height:14pt}
                .marker {font-weight: bold; color: black;text-decoration: none;}
                .version {color: gray;}
                .error {margin-bottom: 10px;}
                .expandable { text-decoration:underline; font-weight:bold; color:navy; cursor:hand; }
                @media screen and (max-width: 639px) {
                    pre { width: 440px; overflow: auto; white-space: pre-wrap; word-wrap: break-word; }
                }
                @media screen and (max-width: 479px) {
                    pre { width: 280px; }
                }
                


        Server Error in '/GasLeakMapWeb' Application. 
            Session state has created a session id, but cannot save it because the response was already flushed by the application.   

            Description:  An unhandled exception occurred during the execution of the current web request. Please review the stack trace for more information about the error and where it originated in the code.

                    
            Exception Details:  System.Web.HttpException: Session state has created a session id, but cannot save it because the response was already flushed by the application. 
        Source Error:   





        An unhandled exception was generated during the execution of the current web request. Information regarding the origin and location of the exception can be identified using the exception stack trace below. 




        Stack Trace:   





        [HttpException (0x80004005): Session state has created a session id, but cannot save it because the response was already flushed by the application.]
            System.Web.SessionState.SessionIDManager.SaveSessionID(HttpContext context, String id, Boolean& redirected, Boolean& cookieAdded) +596
            System.Web.SessionState.SessionStateModule.CreateSessionId() +94
            System.Web.SessionState.SessionStateModule.DelayedGetSessionId() +106
            System.Web.SessionState.SessionStateModule.OnReleaseState(Object source, EventArgs eventArgs) +770
            System.Web.SessionState.SessionStateModule.OnEndRequest(Object source, EventArgs eventArgs) +179
            System.Web.SyncEventExecutionStep.System.Web.HttpApplication.IExecutionStep.Execute() +194
            System.Web.HttpApplication.ExecuteStepImpl(IExecutionStep step) +213
            System.Web.HttpApplication.ExecuteStep(IExecutionStep step, Boolean& completedSynchronously) +91






        Version Information:  Microsoft .NET Framework Version:4.0.30319; ASP.NET Version:4.7.3429.0

                    


            
        [HttpException]: Session state has created a session id, but cannot save it because the response was already flushed by the application.
            at System.Web.SessionState.SessionIDManager.SaveSessionID(HttpContext context, String id, Boolean& redirected, Boolean& cookieAdded)
            at System.Web.SessionState.SessionStateModule.CreateSessionId()
            at System.Web.SessionState.SessionStateModule.DelayedGetSessionId()
            at System.Web.SessionState.SessionStateModule.OnReleaseState(Object source, EventArgs eventArgs)
            at System.Web.SessionState.SessionStateModule.OnEndRequest(Object source, EventArgs eventArgs)
            at System.Web.HttpApplication.SyncEventExecutionStep.System.Web.HttpApplication.IExecutionStep.Execute()
            at System.Web.HttpApplication.ExecuteStepImpl(IExecutionStep step)
            at System.Web.HttpApplication.ExecuteStep(IExecutionStep step, Boolean& completedSynchronously)
            
        This error page might contain sensitive information because ASP.NET is configured to show verbose error messages using &lt;customErrors mode="Off"/&gt;. Consider using &lt;customErrors mode="On"/&gt; or &lt;customErrors mode="RemoteOnly"/&gt; in production environments. 
    '
    soup = BeautifulSoup(html_data, 'html.parser')                      # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
    text = soup.find_all(text=True)                                     
    print(type(html_data))
    # jsonStr = ''                                                        # turning text to string from so i can use pandas to turn it to dictionary
    # try:
    #     for t in text:
    #         jsonStr += '{} '.format(t)
    #     jsonDict = pd.read_json(jsonStr, orient='records')                  # Turning the json string to a dictionary
    # except:
    #     print("Couldnt get the jso




    # 2) GET JSON DATA: from a JSON file and add to the JSON Dictionary: 
    # try:
    #     jsonDict = pd.read_json(jsonFile, orient='records')           # ***jsonDict[properties[i]/colStr(dot properties)][j/rowsnumber(dots)]
    # except:
    #     print("error")
    #     s = str(jsonFile)
    #     # print(s)
    #     jsonStr = ''                                                        # turning text to string from so i can use pandas to turn it to dictionary
    #     for t in text:
    #         jsonStr += '{} '.format(t)
    
    # # 2) GET JSON DATA: Webscrape and sanitize the html response which is usually just the JSON data from the url and add to the JSON Dictionary: 
    # res = requests.get(url)
    # html_data = res.content                                             # Getting the HTML JSOn data 
    # soup = BeautifulSoup(html_data, 'html.parser')                      # parsing the html data with html parcer (can do stuuf like soup.title to get the title, soup.div, soup.li etc)
    # text = soup.find_all(text=True)                                     
    # jsonStr = ''                                                        # turning text to string from so i can use pandas to turn it to dictionary
    # try:
    #     for t in text:
    #         jsonStr += '{} '.format(t)
    #     jsonDict = pd.read_json(jsonStr, orient='records')                  # Turning the json string to a dictionary
    # except:
    #     print("Couldnt get the json data so will re-run function. This is Run "+ str(scrapingCount))
    #     print("***printing error jsonStr\n"+jsonStr)
    #     print("\n***ENDED printing error jsonStr\n")
    #     print("***printing error jsonDict "+ str(jsonDict))
    #     print("\n***ENDED printing error jsonDict \n")
    #     WebscraperJsonToCSV()













#     # 3) CHECK WHAT TICKETS WE ALREADY GOT FROM THE .CSV FILE: Read the csv file and add "TicketNumbers" to the "ticketSet" and print ticketNumber to ticketList.txt" for storage: 
#     csvData = pd.read_csv(csvFile)                                      # ***csvData[colStr][rowNumber]
#     outTXT = open(ticketListFile,"w+")                                  # Settign up to write to txt file
#     for row in range(0,len(csvData)):
#         ticketSet.add(str(csvData["TicketNumber"][row]))    
#         outTXT.write(str(csvData["TicketNumber"][row])+"\n")

#     # 4) CHECK IF NEW TICKET: See if the tickets in "jsonDict" are in "ticketDict". If we have have it, add to "ticketDic", and .txt and .csv file for stoage. If we have it, skip this row since we have this info already. 
#     for row in range(0, len(jsonDict)):
#         if jsonDict["TicketNumber"][row] not in ticketSet:              # If we DONT have this ticket add it
#             isNewTicket = True                                          # This is a new ticket so push the new files
#             print(str(jsonDict["TicketNumber"][row])+ " not in set so adding it")
#             ticketSet.add(jsonDict["TicketNumber"][row])
#             outTXT.write(jsonDict["TicketNumber"][row]+"\n")            # add new ticket to txt file  
#             with open(csvFile,'a') as outCSV:                           # Write the new Ticket object to csv file
#                 s=""
#                 for col in range(0, len(properties)-1):                 # go through each column/dot property
#                     if properties[col] == "DateReported":               # Need to change the Microsoft time to mm/dd/yyyy
#                         s+=turnToDatetime(str(jsonDict[properties[col]][row]))
#                     else: 
#                         s+=str(jsonDict[properties[col]][row])
#                     if col != len(properties)-2:
#                         s+=',' 
#                 s+="\n"
#                 outCSV.write(s)                                         # add new ticket obj to csv file  
#     # 5) Push to Github if we have a new ticket
#     # if (isNewTicket == True):
#     #     git_push()
#     #     isNewTicket == False
#     print("Run Done " + str(scrapingCount))

# # 6) RESCAN FOR TICKETS every x time using sceduler
# scheduler = BlockingScheduler()
# scheduler.add_job(WebscraperJsonToCSV, 'interval', minutes=30)
# scheduler.start()
x=1
while x == 1:
    WebscraperJsonToCSV()
    x=2



