# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 22:08:39 2021

@author: Reitm
"""
import io, os
import configparser
import zipfile
import requests
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox


def initiate(ConfigFile,OutputFolder):
  
    #Calling Config File
    config = configparser.ConfigParser()
    config.read(ConfigFile)
                
    try:
        Survey_ID =config.get("QualtricsIDs", "Survey_ID")
        User_ID = config.get("QualtricsIDs", "User_ID")
        Org_ID = config.get("QualtricsIDs", "Org_ID")
        Datacenter_ID = config.get("QualtricsIDs", "Datacenter_ID")
        API_token  =config.get("QualtricsIDs", "API_token")
    except:
        throwerror('Reading Config Error', "Error: could not read Config file","check you selected a Config file")

    # Setting static parameter
    url = "https://{0}.qualtrics.com/API/v3/surveys/{1}/export-responses/".format(Datacenter_ID , Survey_ID)
    headers = {
        "content-type": "application/json",
        "x-api-token": API_token,
        }
    
    # Step 1: Creating Data Export
    data = {
            "format": "csv",
            "seenUnansweredRecode": -1
           }
    
    downloadRequestResponse = requests.request("POST", url, json=data, headers=headers)
    print(downloadRequestResponse.json())
    
    try:
        downloadRequestResponse.json()["result"]["progressId"]
    except KeyError:
        throwerror('Download Initiation Error', "Error: Could not initiate download:","check Qualtrics IDs are correct")
            
    return downloadRequestResponse, url, headers

def checkprogress(downloadRequestResponse,url,headers):
    progressId = downloadRequestResponse.json()["result"]["progressId"]
    requestCheckUrl = url + progressId
    requestCheckResponse = requests.request("GET", requestCheckUrl, headers=headers)
    requestCheckProgress = requestCheckResponse.json()["result"]["percentComplete"]
    progressStatus = requestCheckResponse.json()["result"]["status"]
    fileId = None
    isFile = None
    try:
        fileId = requestCheckResponse.json()["result"]["fileId"]
        isFile = requestCheckResponse.json()["result"]["fileId"]
    except KeyError:
        pass
    return requestCheckProgress, progressStatus, fileId, isFile


def downloadsurveys(OutputFolder,url,headers,fileId):

    # Step 3: Downloading file
    thisdir = os.getcwd()
    os.chdir(OutputFolder)  
    
    requestDownloadUrl = url + fileId + '/file'
    requestDownload = requests.request("GET", requestDownloadUrl, headers=headers, stream=True)
    
    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(requestDownload.content)).extractall("MyQualtricsDownload")
    
    now = datetime.now()
    today = now.strftime("%Y_%m_%d")
    if os.path.isdir(OutputFolder+"/SurveyResponses_"+today):
        today = now.strftime("%Y_%m_%d_%H_%M_%S")
       
    os.rename(OutputFolder+"/MyQualtricsDownload",OutputFolder+"/SurveyResponses_"+today)    
    os. chdir(thisdir)  

    print("Download Complete")
    
def throwerror(ErrorType, Message, Message2=None):
    msg = QMessageBox()
    msg.setText(Message)
    msg.setStyleSheet(
        "QLabel{min-width:400 px; font-family: Arial; font-size: 42px;}"
        "QPushButton{ width:250px; font-family: Arial;font-size: 24px;}"
                      );

    msg.setIcon(QMessageBox.Warning)
  

    if Message2:
        msg.setInformativeText(Message2)

    msg.setWindowTitle(ErrorType)
    msg.exec_()    
