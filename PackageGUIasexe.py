# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 10:52:32 2021

@author: Reitm
"""
import PyInstaller.__main__
import os
import configparser

# exename = 'QualtricsDownloader_V1.0'
# run once to make initial spec script
PyInstaller.__main__.run([
    'driveGui_v1.0.spec',
    '--onedir',
    '--noconfirm',
    # '-n', exename
])


#  modify spec script to include UIs and SetupFiles

# add the following to the spec script
path = os.getcwd()
# folderstoadd = [
#          (path +'/SetupFiles/*', "SetupFiles"), 
#          (path +'/GUIWindows/*', "GUIWindows"),
#          ]
# and then make datas = folderstoadd,

# change .py to .spec on line 11 and then run again

# necessary for the GUI webpage viewer
os.chdir(path + '/dist/driveGui_v1.0/')
config = configparser.ConfigParser()
config.add_section('Paths')
config.set('Paths', 'Prefix', 'PyQt5/Qt')

with open('qt.conf', 'w') as configfile:
    config.write(configfile) 

os.chdir(path + '/dist/driveGui_v1.0/PyQt5/Qt/bin')
config = configparser.ConfigParser()
config.add_section('Paths')
config.set('Paths', 'Prefix', '..')

with open('qt.conf', 'w') as configfile:
    config.write(configfile) 