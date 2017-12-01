# ============================================================
#
# Script: rotatelogs.py
#
# Author: Dirk Nachbar, https/dirknachbar.blogspot.ch
#
# Purpose: Rotates the WebLogic Server Logfiles for a list
#          of given Servers, either AdminServer or Managed Servers
#
# ============================================================
 
# Imports 
import sys
from java.io import File
from java.io import FileOutputStream
from java.io import FileInputStream
 
servers_list=''
configfile=''
 
def helpUsage():
    print 'Usage: rotatelogs.py -help'
    print '          [-servers] list of Servers, delimited by :'
    print '          [-props] properties file for connect to AdminServer'
    print 'E.g.:  wlst.sh rotatelogs.py -servers DEMOMS1:DEMOMS2 -props /home/oracle/domain.properties'
    exit()
 
def connectAdmin():
    connect(adminUserName,adminPassword,adminURL)
 
for i in range(len(sys.argv)):
    if sys.argv[i] == "-help":
        helpUsage()
    elif sys.argv[i] == "-servers":
        if i+1 < len(sys.argv):
            servers_list = sys.argv[i+1]
    elif sys.argv[i] == "-props":
        if i+1 < len(sys.argv):
            configfile = sys.argv[i+1]
 
if len(servers_list)==0 or len(configfile)==0:
    print 'Missing required arguments (-servers, -props)'
    print ''
    helpUsage()
 
propInputStream = FileInputStream(configfile)
configProps = Properties()
configProps.load(propInputStream)
adminURL=configProps.get("admin.url")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")

connectAdmin()
 
domainRuntime()
 
servers=servers_list.split(":")
 
for server in servers:
    print '================================================'
    print 'Current Server: ' +server
    cd('/ServerRuntimes/'+server+'/ServerLogRuntime/'+server)
    print 'Rotating Logfile for Server: ' +server
    cmo.forceLogRotation()
    print '================================================'

