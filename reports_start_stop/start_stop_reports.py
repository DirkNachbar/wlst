# ============================================================
#
# Script: start_stop_reports.py
#
# Author: Dirk Nachbar, http://dirknachbar.blogpost.com
#
# Purpose: Start / Stop Script for a list of Oracle Reports Servers
#
# ============================================================
 
import sys
import re
import os
from datetime import datetime
from java.io import File
from java.io import FileOutputStream
from java.io import FileInputStream
  
func=''
propfile=''
  
def helpUsage():
   print 'Usage: start_stop_reports.py [-help]'
   print '      [-function] provide function either start or stop'
   print '      [-propfile] provide the property file'
   exit()
  
for i in range(len(sys.argv)):
   if sys.argv[i] in ("-help"):
           helpUsage()
   elif sys.argv[i] in ("-function"):
           if i+1 < len(sys.argv):
                   func = sys.argv[i+1]
   elif sys.argv[i] in ("-propfile"):
           if i+1 < len(sys.argv):
                   propfile = sys.argv[i+1]
  
if len(func)==0 or len(propfile)==0:
   print 'Missing required arguments (-func, -propfile)'
   print ' '
   helpUsage()
  
# Load Connection Properties
propInputStream = FileInputStream(propfile)
configProps = Properties()
configProps.load(propInputStream)
nmPort=configProps.get("nm.port")
nmHost=configProps.get("nm.host")
nmPassword=configProps.get("nm.password")
nmUser=configProps.get("nm.username")
domainName=configProps.get("domain.name")
domainHome=configProps.get("domain.home")
reportsServers=configProps.get("reports.servers")
  
# Connect to Node Manager
nmConnect(nmUser, nmPassword, nmHost, nmPort, domainName, domainHome, 'ssl')
  
# Perform startup of defined Oracle Reports Servers
if func=="start":
   print 'Starting configured Reports Servers'
   for repserver in reportsServers.split(','):
      print 'Starting Reports Server: ' +repserver
      nmStart(serverName=repserver, serverType='ReportsServerComponent')
  
# Perform stop of defined Oracle Reports Servers
if func=="stop":
   print 'Stopping configured Reports Servers'
   for repserver in reportsServers.split(','):
      print 'Stopping Reports Server: ' +repserver
      nmKill(serverName=repserver, serverType='ReportsServerComponent')

