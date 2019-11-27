#!/usr/bin/env python
# Envia logs em CEF para o SmartConnector
# do ArcSight a partir de um arquivo CSV 
# Requisito: pip install cefevent
# Codigo desenvolvido para Python3
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

# Variaveis utilizadas
print("[INFO] Inicializando variaveis de ambiente")
currentFilespath = 'C:\\SEPStatusIntegration\\'
oldFilesPath = 'C:\\SEPStatusIntegration\\oldFiles\\'
fileExtention = 'csv'
syslogServer = '0.0.0.0'
syslogPort = 516
arquivosCSV = ''

# Busca os arquivos CSV da pasta definida
def buscaArquivosCSV():
    print("[INFO] Fazendo busca por arquivos")
    try:
        os.chdir(currentFilespath)
        global arquivosCSV
        arquivosCSV = glob.glob('*.{}'.format(fileExtention))
    except:
        print('[ERROR] Nao foi possivel ler os arquivos e/ou caminhos especificados')
        

# Trata os eventos CEF para remover chars desncessarios
def trataCEF(eventoCEF):
    print("[INFO] Tratando o evento CEF")
    subcef = str(eventoCEF)
    cefcef = re.sub('<bound method CEFEvent.build_cef of ', '', subcef)
    ceflen = len(cefcef) - 1
    cef = "\n" + str(cefcef[:ceflen])
    return cef

# Faz o envio do evento via SYSLOG
def enviaCEF(eventoCEFTratado):
    print("[INFO] Enviando o evento CEF")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(eventoCEFTratado.encode(), (syslogServer, syslogPort))
        sock.close()
    except socket.error:
        print('[ERROR] Erro no envio do syslog')

if __name__ == '__main__':
    # Le o arquivo
    buscaArquivosCSV()
    for arquivo in arquivosCSV:
        print("[INFO] Realizando o parser do arquivo: " + arquivo)
        with open(arquivo, 'r') as csvfile:
            # Remove o header do arquivo para nao enviar via CEF
            readCSV = csv.reader(csvfile, delimiter=',')
            header = next(readCSV)
            for row in readCSV:
                # Campos obritatorios
                c = CEFEvent()
                c.set_field('name', 'SEP Inventory')
                c.set_field('deviceVendor', 'Symantec')
                c.set_field('deviceProduct', 'Altiris')
                
                # Campos customizados
                c.set_field('deviceHostName', row[1])
                c.set_field('deviceAddress', row[2])
                
                c.set_field('deviceCustomString1Label', 'System Type')
                c.set_field('deviceCustomString1', row[3])
                
                c.set_field('deviceCustomString1Label', 'OS Name')
                c.set_field('deviceCustomString2', row[4])
                
                c.set_field('deviceCustomDate1Label', 'Client Date')
                c.set_field('deviceCustomDate1', row[5])
                
                c.set_field('deviceCustomString3Label', 'AV Status')
                c.set_field('deviceCustomString3', row[6])
                
                c.set_field('deviceCustomString3Label', 'State')
                c.set_field('deviceCustomString3', row[8])
                
                c.set_field('deviceCustomString4Label', 'State')
                c.set_field('deviceCustomString4', row[8])

                c.set_field('deviceCustomString5Label', 'Version')
                c.set_field('deviceCustomString5', row[13])
                
                c.set_field('deviceCustomDate2Label', 'Last successful AV scan')
                c.set_field('deviceCustomDate2', row[14])
                
                c.set_field('deviceCustomNumber1Label', 'Virus definition revision in use')
                c.set_field('deviceCustomNumber1', row[15])
                
                c.set_field('deviceCustomString6Label', 'SEP installed')
                c.set_field('deviceCustomString6', row[23])
                                
                # Faz a tratativa do CEF
                cef = trataCEF(c.build_cef)
                
                # Faz o envio do CEF via syslog
                enviaCEF(cef)
                time.sleep(1)

        # Move arquivo de lugar para a pasta OldFiles
        print("[INFO] Movendo o arquivo " + arquivo + " para a pasta oldFiles")
        shutil.move(currentFilespath+arquivo, oldFilesPath+arquivo)
