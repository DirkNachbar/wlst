# ============================================================
#
# Script: soa_iws_report.py
#
# Author: Dirk Nachbar
#
# Purpose: Generates an IWS Report based on input time range
#
# ============================================================
 
import sys, os, getopt
from java.util import Date
from java.text import SimpleDateFormat
from java.io import File
from java.io import FileOutputStream
from java.io import FileInputStream
 
# Load the WLS Connection Credential and establish the connection
propInputStream = FileInputStream(sys.argv[1]+".properties")
# propInputStream = FileInputStream("domain.properties")
configProps = Properties()
configProps.load(propInputStream)
domainName=configProps.get("domain.name")
soaURL=configProps.get("soa.url")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")
LogFile=os.environ['TheLogFile']
 
connect(adminUserName,adminPassword,soaURL)
 
getSoaIWSReportByDateTime(sys.argv[1], 0, sys.argv[2], sys.argv[3], 'default', None, 10, 'html', LogFile)
disconnect()

