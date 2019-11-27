# Scenario
I had to pull data from Altiris e push to ArcSight. To do so, I have scheduled a report at Altiris that export a list of assets and their current SEP status. This script takes this CSV file, convert into CEF format and send using syslog to the Arcsight SmartConnector using UDP. 

# Requirements
This is script is based on the Kamus Hadenes script. In order to the script to run it is mandatory to install the 
[cefevent](https://github.com/kamushadenes/cefevent/tree/master/cefevent) by [Kamus Hadenes](https://github.com/kamushadenes)

`pip install cefevent`

Download the folder in his Github page and run the script from there.

# What need to be changed
In the "VARIABLES" section there are variables such as script folder, file extention, syslog info. They need to be changed accordingly. In the main section, there are a bunch of "c.set_field" that need to be changed according to your CSV file. The header of the CEF file (device vendor, device product, name, and others) also requires a change.
