# Hiwi_Katarina
Climate Data Set 


## Installed Packages and Versions

This project uses the following key Python packages and their versions:

* aiohttp: 3.9.5
* anaconda-client: 1.11.0
* autopep8: 1.6.0
* bokeh: 2.4.3
* flask: 1.1.2
* jupyterlab: 3.4.4
* matplotlib: 3.9.4
* numpy: 1.24.4
* pandas: 1.4.4
* scikit-learn: 1.0.2
* scipy: 1.13.1
* seaborn: 0.11.2
* torch: 2.2.2
* torchvision: 0.17.2
* ultralytics: 8.3.56
  
For the full list of installed packages and versions, refer to the requirements.txt file or the detailed package output.


## TWO FOLDER 

1. Link Validation and Tweet Categorization Script- update_automation
/Hiwi_Katarina/update_automation/extended_version

### Overview

This script processes a JSON file containing image links, validates their accessibility, replaces broken links with available alternatives, and categorizes tweets based on their content. It also logs deleted links, generates statistics, and exports data to CSV format.

### Features

* Validates image links: Checks if the main link is accessible and replaces it with a valid alternative if available.
* Logs deleted links: Stores broken links along with their metadata in a log file.
* Generates statistics: Tracks the number of deleted links per category and over time.
* Categorizes tweets: Uses NLTK to analyze and assign tweets to predefined categories.
* Exports data to CSV: Saves details of deleted links in a structured CSV file.

### Methods 

Functions Overview

* Link Validation
    * validate_link(link): Checks if a given link is accessible.
    * validate_links(alternatives): Returns a list of valid alternative links.
* Processing and Logging
    * process_links(file_path, log_path): Processes and updates links, logs removed ones.
    * export_deleted_links_to_csv(deleted_links, csv_path): Saves deleted links to a CSV file.
* Tweet Categorization
    * categorize_tweet(tweet_context): Categorizes tweets based on keywords.


### FLOW

Dependencies : pip install requests nltk

* python update_automation.py
* python tweet_categorization.py


### Output Files
* image_links.json → Updated JSON with replaced links
* link_check.log → Log file with deleted links and statistics
* deleted_links.csv → CSV file containing details of removed links

2. Violence Detection in Image Data Set - violence_detection