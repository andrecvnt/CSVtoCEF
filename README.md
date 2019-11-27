# Scenario
I had to pull data from Altiris e push to ArcSight. To do so, I have schedule a report at Altiris that export a list of assets and their current SEP status. This script takes this CSV file, convert into CEF format and send using syslog to the Arcsight SmartConnector using UDP. 

# Requirements
This is script is based on the Kamus Hadenes script. In order to script run it is mandatory to install the 
[cefevent](https://github.com/kamushadenes/cefevent/tree/master/cefevent) by [Kamus Hadenes](https://github.com/kamushadenes)

`pip install cefevent`

Download the folder in his Github page and run the script from there.
