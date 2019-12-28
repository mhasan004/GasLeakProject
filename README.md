# GasLeakProject
An interactive web application that will visualize the locations of all reported gas leaks in New York using Python Dash. Will predict areas that are less likely to report gas leaks and will analyze the socioeconomic conditions in those areas. 

# conEd_SceduledWebscraperJsonCSV.py
**Location:** GettingDataFrom_ConEd/conEd_SceduledWebscraperJsonCSV.py
**Description:**
This Python script periodically scrapes gas leak report from the ConEdison website and appends the data of new gas leak reports to * *UNION.csv* * and * *ticketList.txt* * files and pushes the changes to GitHub so that I can have the latest history.

**Installing Required Packages**
Run * *GettingDataFrom_ConEd/requirements.txy* * using * *bash requirements.txt* * to install the required packages to run this script.

**USES:** 
* Can get JSON data from a url and convert the objects into a csv file. Will need to change the *url*, *csvFile*, and *properties* variables to fit the specific needs.
* Can get JSON data from a JSOn file and store objects into a csv file. Will need to change the *url*, *csvFile*, *jsonFile* , and *properties* variables.
* To push changes to github, the *PATH_OF_GIT_REPO* (where the *.git* file is located) and *COMMIT_MESSAGE* needs to be changed


