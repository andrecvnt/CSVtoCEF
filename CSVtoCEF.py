#!/usr/bin/env python
# Send logs to Arcsight SmartConnector from Arcsight 
# using a CSV file as source
# Requirements: python3 and cefevent (pip install cefevent)
# by Andre C.
#

import socket
import sys
import time
from cefevent import CEFEvent, CEFSender
import csv
import re
import os
import glob
import shutil

# VARIABLES
print("[INFO] Starting the environment variables")
currentFilespath = 'C:\\SEPStatusIntegration\\'
oldFilesPath = 'C:\\SEPStatusIntegration\\oldFiles\\'
fileExtention = 'csv'
syslogServer = '10.20.29.73'
syslogPort = 516
arquivosCSV = ''

# SEARCH FOR CSV FILES IN THE DEFINED FOLDER
def buscaArquivosCSV():
    print("[INFO] Searching files")
    try:
        os.chdir(currentFilespath)
        global arquivosCSV
        arquivosCSV = glob.glob('*.{}'.format(fileExtention))
    except:
        print('[ERROR] Error reading files')

# REMOVE UNNECESSARY CHARS FROM THE CEF
def trataCEF(eventoCEF):
    print("[INFO] Removing unnecessary chars from EventID" + str(linhaDoCSV))
    subcef = str(eventoCEF)
    cefcef = re.sub('<bound method CEFEvent.build_cef of ', '', subcef)
    ceflen = len(cefcef) - 1
    cef = "\n" + str(cefcef[:ceflen])
    return cef

# SEND LOGS VIA SYSLOG
def enviaCEF(eventoCEFTratado):
    print("[INFO] Sending CEF EventID " + str(linhaDoCSV))
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(eventoCEFTratado.encode(), (syslogServer, syslogPort))
        sock.close()
    except socket.error:
        print('[ERROR] Error sending events')

if __name__ == '__main__':
    # READ FILE
    buscaArquivosCSV()
    for arquivo in arquivosCSV:
        with open(arquivo, 'r') as csvfile:
            # REMOVE CSV HEADER
            readCSV = csv.reader(csvfile, delimiter=',')
            header = next(readCSV)
            linhaDoCSV = 0
            for row in readCSV:
                linhaDoCSV += 1
                # THESE FIELDS ARE STATIC
                c = CEFEvent()
                c.set_field('name', 'SEP Inventory')
                c.set_field('deviceVendor', 'Symantec')
                c.set_field('deviceProduct', 'Altiris')
                
                # THESE FIELDS WILL VARY BASED ON THE CSV LINES
                c.set_field('deviceHostName', row[1])
                c.set_field('deviceAddress', row[2])
                c.set_field('deviceCustomString1Label', 'System Type')
                c.set_field('deviceCustomString1', row[3])
                c.set_field('deviceCustomString1Label', 'OS Name')
                c.set_field('deviceCustomString2', row[4])
                c.set_field('deviceCustomString3Label', 'AV Status')
                c.set_field('deviceCustomString3', row[6])
                c.set_field('deviceCustomString3Label', 'State')
                c.set_field('deviceCustomString3', row[8])
                c.set_field('deviceCustomString4Label', 'State')
                c.set_field('deviceCustomString4', row[8])
                c.set_field('deviceCustomString5Label', 'Version')
                c.set_field('deviceCustomString5', row[13])
                c.set_field('deviceCustomNumber1Label', 'Virus definition revision in use')
                c.set_field('deviceCustomNumber1', row[15])
                c.set_field('deviceCustomString6Label', 'SEP installed')
                c.set_field('deviceCustomString6', row[23])            
                cef = trataCEF(c.build_cef)
                enviaCEF(cef)
                time.sleep(1)

        # Move files to an "old" folder
        print("[INFO] Moving file " + arquivo + " to the oldFiles folder")
        shutil.move(currentFilespath+arquivo, oldFilesPath+arquivo)
