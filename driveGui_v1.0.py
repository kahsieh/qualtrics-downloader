# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 13:56:08 2021

@author: Reitm
"""
import sys, os
import configparser

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog as dlog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

import GQDinGUI
import plot

if getattr(sys, 'frozen', False):
    thisfolder = os.path.dirname(sys.executable)
elif __file__:
    thisfolder = os.path.dirname(os.path.abspath(__file__)) 
    
UserFolder = os.path.dirname(thisfolder)

class PrimaryUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # Call the inherited classes __init__ method
        uic.loadUi(thisfolder+'/GUIWindows/MainGUI.ui',self)
        self.show() # Show the GUI
        
        config = configparser.ConfigParser()
        config.read(thisfolder+'/SetupFiles/GuiMemory.txt')
        pastconfig = config.get("pastconfig", "ConfigFile")
        pastOD = config.get('pastOD','OutputFolder')
        
        if pastconfig:
            self.ConfigFileTxt.setText(pastconfig)
        if pastOD:
            self.OutputDirectoryTxt.setText(pastOD)
            
        #set menubar functions    
        self.actionAbout.triggered.connect(self.About)  
        self.actionFyQIDs.triggered.connect(self.FindQualtricsIDsHelp)  

    def About(self):
        self.abwin= AboutWindow()
        self.abwin.show()
        
    def FindQualtricsIDsHelp(self):
        self.FWIHwin= FindQualtricsIDsWindow()
        self.FWIHwin.show()
    
    def CreateConfig(self):
        self.cfgwin= ConfigUi()
        self.cfgwin.show()

    def ChooseConfig(self):
        if str(self.ConfigFileTxt.text()):
            ConfigFile,_ = dlog.getOpenFileName(None, "Select Config File",str(self.ConfigFileTxt.text())) # Ask for file
        else:
            ConfigFile,_ = dlog.getOpenFileName(None, "Select Config File", UserFolder) # Ask for file

        ConfigFile = str(ConfigFile)
        self.ConfigFileTxt.setText(ConfigFile)
        return ConfigFile

    def ChooseOutput(self):
        if str(self.OutputDirectoryTxt.text()):
            OutputFolder = dlog.getExistingDirectory(None, "Select Output Directory",str(self.OutputDirectoryTxt.text()))
        else:
            OutputFolder = dlog.getExistingDirectory(None, "Select Output Directory", UserFolder)

        OutputFolder = str(OutputFolder)
        self.OutputDirectoryTxt.setText(OutputFolder)
        return OutputFolder

    def DownloadQualtrics(self):
        # Set the paths to configuration file and folder for survey results
        ConfigFile = str(self.ConfigFileTxt.text())
        ConfigFile = ConfigFile.replace(os.sep,'/')
        
        OutputFolder = str(self.OutputDirectoryTxt.text())
        OutputFolder = OutputFolder.replace(os.sep,'/')

        # initiate the download
        downloadRequestResponse, url, headers = GQDinGUI.initiate(ConfigFile,OutputFolder)
        
        # check the progress
        isFile = None
        progressStatus = "inProgress"
        
        while progressStatus != "complete" and progressStatus != "failed" and isFile is None:
            requestCheckProgress, progressStatus, fileId, isFile = GQDinGUI.checkprogress(downloadRequestResponse,url,headers)
            self.progressBar.setValue(int(requestCheckProgress))
            print(requestCheckProgress)
            
        #download the results
        GQDinGUI.downloadsurveys(OutputFolder,url,headers,fileId)
        
        #remember the last succesful settings to autoload for next time
        if progressStatus == "complete":
            config = configparser.ConfigParser()
            config.read(thisfolder+'/SetupFiles/GuiMemory.txt')
            config["pastconfig"]["ConfigFile"] = ConfigFile
            config["pastOD"]["OutputFolder"] = OutputFolder
            with open(thisfolder+'/SetupFiles/GuiMemory.txt', 'w') as outputfile:
                    config.write(outputfile)    

    def ChooseCsvFile(self):
        if str(self.CsvFileTxt.text()):
            CsvFile,_ = dlog.getOpenFileName(None, "Select CSV File",str(self.CsvFileTxt.text())) # Ask for file
        else:
            CsvFile,_ = dlog.getOpenFileName(None, "Select CSV File", UserFolder) # Ask for file

        CsvFile = str(CsvFile)
        self.CsvFileTxt.setText(CsvFile)
        return CsvFile

    def LoadCsvFile(self):
        CsvFile = str(self.CsvFileTxt.text())
        CsvFile = CsvFile.replace(os.sep,'/')
        self.ColumnNameTxt.clear()
        self.ColumnNameTxt.addItems(plot.listPlottableColumnsInCsv(CsvFile))

    def Plot(self):
        CsvFile = str(self.CsvFileTxt.text())
        CsvFile = CsvFile.replace(os.sep,'/')
        plot.plotColumnByDescription(CsvFile, self.ColumnNameTxt.currentText())
        

class ConfigUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # Call the inherited classes __init__ method
        uic.loadUi(thisfolder+'/GUIWindows/CreateConfigWindow.ui',self)
        self.show()

    def saveConfigFile(self):
        config = configparser.ConfigParser()
        config.read(thisfolder+'/SetupFiles/ConfigFileTemplate.txt')
        
        config["QualtricsIDs"]["Survey_ID"] = self.SurveyID.text()
        config["QualtricsIDs"]["User_ID"] = self.UserID.text()
        config["QualtricsIDs"]["Org_ID"] = self.OrgID.text()
        config["QualtricsIDs"]["Datacenter_ID"] = self.DatacenterID.text()
        config["QualtricsIDs"]["API_token"] = self.API_Token.text()
        ConfigFile,_ = dlog.getSaveFileName(None, "Select Config File Name and Directory", UserFolder + "/myconfig.txt" )
        ConfigFile = str(ConfigFile)
        
        if ConfigFile:
            if not ConfigFile.lower().endswith('.txt'):
                ConfigFile  = ConfigFile+".txt"

            with open(ConfigFile, 'w') as outputfile:
                config.write(outputfile)        
            
            self.ConfigFile =ConfigFile
            
        self.close()


class AboutWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__() # Call the inherited classes __init__ method
        uic.loadUi(thisfolder+'/GUIWindows/AboutWindow.ui',self)
        self.show()
        
           
class FindQualtricsIDsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.qualtrics.com/support/integrations/api-integration/finding-qualtrics-ids/#LocatingQualtricsIDs"))
        self.setCentralWidget(self.browser)
        self.browser.setZoomFactor(2.5)
        self.showMaximized()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = PrimaryUi()
    app.exec_()


# Execute main function
if __name__ == '__main__':
    main()




    
