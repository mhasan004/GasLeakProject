# GasLeakProject
An interactive web application that will visualize the locations of all reported gas leaks in New York using Python Dash. Will predict areas that are less likely to report gas leaks and will analyze the socioeconomic conditions in those areas. 

# The ConEdison JSON Scraper
**File Location:** Getting_GasLeak_Data/conEd_ScraperJsonCSV.py

**Description:**
This Python script periodically scrapes gas leak report from the ConEdison website and appends the data of new gas leak reports to *conEd_GasHistory.csv* and *conEd_TicketList.txt* files and pushes the changes to GitHub so that I can have the latest gas leak report history.

**Installing Required Packages**
Run the *requirements.txt* file in *Getting_GasLeak_Data* folder using the command *bash requirements.txt* to install the required packages.

**Uses:** 
* Get JSON data from a url and convert the objects into a csv file. Will need to change the *url*, *csvFile*, and *properties* variables to fit the specific needs.
* Get JSON data from a JSON file and store objects into a csv file. Will need to change the *url*, *csvFile*, *jsonFile* , and *properties* variables.
* Automatically push changes to github when script finds new JSON objects. Change the *PATH_OF_GIT_REPO* (where the *.git* file is located) and *COMMIT_MESSAGE* variables.


