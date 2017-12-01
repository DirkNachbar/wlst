#!/bin/ksh
#
# Author: Dirk Nachbar
#
# Purpose: Script to create an IWS Report for a given SOA Domain
#          and Managed Server
#
#---------------------------------------------------------------------
 
 
#---------------------------------------------------------------------
# CONSTANTS
#---------------------------------------------------------------------
MyName="$(basename $0)"
# Align the value for your Middleware Home directory
MW_HOME=/u00/app/oracle/product/fmw-soa-12.2.1.2.0
WorkDir=`pwd`
 
 
#---------------------------------------------------------------------
Usage()
#
# PURPOSE: Verwendung
#---------------------------------------------------------------------
{
 
  echo "ERR: create_soa_iws_report.ksh called with wrong parameters"
  cat <<_EOI
 
SYNOPSIS
       create_soa_iws_report.ksh  -d <Domain_Name> -s <ManagedServer> 
               -t <Number of Hours to look back>
                
DESCRIPTION
        
Creation of IWS Report for a given SOA Domain and Managed Server
 
_EOI
 
 
    exit 1
}
 
#---------------------------------------------------------------------
CheckParams()
#
# PURPOSE: Checks the input Parmeters 
#---------------------------------------------------------------------
{
    if [ "${TheDomain}" = "" ] ; then
        echo "ERR: Missing parameter(s), the flags -d must be used."
        Usage
    fi
 
    if [ "${TheManagedServer}" = "" ] ; then
        echo "ERR: Missing parameter(s), the flags -s must be used."
        Usage
    fi
 
    if [ "${TheHoursBack}" = "" ] ; then
        echo "ERR: Missing parameter(s), the flags -t must be used."
        Usage
    fi
 
}
 
 
#---------------------------------------------------------------------
CreateIWSReport()
#
# PURPOSE: Creates an IWS Report for the given ManagedServer
#
#---------------------------------------------------------------------
{
 
echo "STARTING: Creating IWS Report for ${TheDomain} / ${TheManagedServer} over the last ${TheHoursBack} hours"
HighDate="$(date '+%Y-%m-%dT%H:%M:%S+0200')"
 
LowDate=$(eval "date '+%Y-%m-%dT%H:%M:%S+0200' -d '${TheHoursBack} hours ago'")
 
LogFileDate="$(date '+%Y-%m-%d_%H:%M:%S')"
 
export TheLogFile=${WorkDir}/logs/iws_report_${TheDomain}_${TheManagedServer}_${LogFileDate}.html
 
 
${MW_HOME}/oracle_common/common/bin/wlst.sh ${WorkDir}/soa_iws_report.py ${TheManagedServer} ${LowDate} ${HighDate}
 
echo "DONE: Creating IWS Report for ${TheDomain} / ${TheManagedServer} over the last ${TheHoursBack} hours"
echo "INFO: IWS Report = ${TheLogFile}"
 
 
}
 
#---------------------------------------------------------------------
MailIWSReport()
#
# PURPOSE: Mail the prior create IWS Report 
#
#---------------------------------------------------------------------
{
 
# Getting the Email Recipients
ConfigFile=${TheManagedServer}.properties

TheMailRecipients="$(cat ${WorkDir}/${ConfigFile} | grep -i "^mailrecipients=" | head -n 1 | cut -d= -f2-)"
TheEmailSubject="IWS for ${TheDomain} - ${TheManagedServer}"
 
echo "STARTING: Mail the IWS Report ${TheLogFile}"
 
echo "IWS Report" | mailx -s "${TheEmailSubject}" -a ${TheLogFile} ${TheMailRecipients}
 
echo "DONE: Mail the IWS Report ${TheLogFile}"
 
}
 
 
#---------------------------------------------------------------------
# MAIN
#---------------------------------------------------------------------
 
TheDomain=""
TheManagedServer=""
TheHoursBack=""
 
while getopts d:s:t:h: CurOpt; do
    case ${CurOpt} in
        d) TheDomain="${OPTARG}"        ;;
        s) TheManagedServer="${OPTARG}" ;;
        t) TheHoursBack="${OPTARG}"     ;;
        h) Usage           exit 1       ;;
        ?) Usage           exit 1       ;;
    esac
done
shift $((${OPTIND}-1))
 
if [ $# -ne 0 ]; then
    Usage
fi
 
 
CheckParams
 
CreateIWSReport
 
MailIWSReport

