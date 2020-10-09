# GasLeakProject
An interactive web application that will visualize the locations of all reported gas leaks in New York using Python Dash. Will predict areas that are less likely to report gas leaks and will analyze the socioeconomic conditions in those areas. 

# The ConEdison Periodic Scraper
## ConEdison Gas Leak Report Scraper program - `scraper_ConEdison.py` 
 * Get the latest gas leak reports using the ConEdison API and then retrieves the census location data using the Census Beru API and then updates all files in `GasLeakCombined/DataFiles/ConEdison`
 * `GasHistory_2010_ConEdisonTracts.csv` - record of all the gas leak report data with its respective census location data. 
 * `GasHistory_2010_ReportFrequency_Hourly.csv`  - lists how many gas leaks reports there were per hour, per census tract, per day 
 * `GasHistory_2010_ReportFrequency_Monthly.csv` - lists how many gas leaks reports there were per month, per census tract

**File Location:** Getting_GasLeak_Data/scraper_ConEdison.py.py

**Description:**
This python script periodically scrapes gas leak report from the ConEdison website and appends the data of new gas leak reports to *GasHistory_ConEdison.csv* and *conEd_TicketList.txt* files and pushes the changes to GitHub so that I can have the latest gas leak report history.

**Installing Required Packages**
Run the *requirements.txt* file in *Getting_GasLeak_Data* folder using the command *bash requirements.txt* to install the required packages.

**Uses:** 
* Get JSON data from a url and convert the objects into a csv file. Will need to change the *url*, *csvFile*, and *properties* variables to fit the specific needs.
* Get JSON data from a JSON file and store objects into a csv file. Will need to change the *url*, *csvFile*, *jsonFile* , and *properties* variables.
* Automatically push changes to github when script finds new JSON objects. Change the *PATH_OF_GIT_REPO* (where the *.git* file is located) and *COMMIT_MESSAGE* variables.

# The New York Fire Department Gas Report Scraper
**File Location:** Getting_GasLeak_Data/scraper_NYFD.py

**Description:**
This python script uses the NYC Open Data API to store all gas related utility emergency reports into a file called *GasHistory_NYFD.csv* 

# Plotting Gas Leak Reports per Census Track per Hour
**File Location:** Getting_GasLeak_Data/

**Description:**
This python script goes through *GasHistory_ConEdison.csv* and uses the Census Bureau's Geocoding API to find what census tract each report was made in adn creates a new file where is keeps track of the number of gas reports reported in that hour for each census track. This data will then be plotted
