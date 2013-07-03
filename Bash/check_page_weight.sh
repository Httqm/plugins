#!/bin/bash

######################################### check_page_weight.sh ######################################
# FUNCTION :    Measure the weight of the given webpage, including its HTML source code and linked
#               files (CSS, JS, images), and warn accordingly.
#
# AUTHOR :      Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :     GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :       1. Full page weight is determined by downloading the HTML source code of the
#                  specified page ("-u" parameter), then downloading all linked objects (images, JS,
#                  CSS). However, some websites host their linked content on a different domain,
#                  i.e. the page 'http://www.example.com' may include images from
#                  'http://static.example.com' and CSS from 'http://www2.example.com'. Content from
#                  these domains won't be retrieved (with wget default options) as following links
#                  carelessly may lead to downloading the whole Internets :-(
#                  To get content from these domains, the "-d" parameter of this plugin instructs
#                  wget to content content from the listed domains only.
#               2. All computation is made assuming 1KB = 1024 bytes (and so on for MB, GB, ...)
#               3. This plugin outputs page weight in bytes, but external graphing tools may
#                  accommodate their Y-scale assuming 1KB = 1000 bytes, i.e. :
#                  654321 B = 639 KB (1 KB = 1024 B), but may be graphed as 654 KB (1 KB = 1000 B).
#
# COMMAND LINE :
#               check_page_weight.sh -u "<URL of page to check>" -d "domains" -w "<warn>" -c "<crit>"
#               check_page_weight.sh -u "http://www.example.com" -d "static.example.com,www2.example.com" -w 50KB -c 100KB -v
#
# VERSION :     20130703
########################################## ##########################################################

absolutePathToCurrentFile=$(cd $(dirname "$0"); pwd)
source "${absolutePathToCurrentFile}/Functions/Common.sh"

########################################## ##########################################################
# FUNCTIONS
########################################## ##########################################################

#---------------------
# Show the plugin help message.
# ARGUMENTS : none
# RETURN    : void
#---------------------
exitShowHelp() {
    cat << GLOUBIBOULGA
    FUNCTION:
        Measure the weight of the given webpage, including its HTML source code and linked
        files (CSS, JS, images), and warn accordingly.

    USAGE:
        $0 -u "<URL of page to check>" -d "domains" -w "<warn>" -c "<crit>"

    EXAMPLE:
        $0 -u "http://www.example.com" -d "static.example.com,www2.example.com" -w 50KB -c 100KB -v

    OPTIONS:
        -h  Show this help
        -u  URL of page to check
        -d  Comma-separated list of domains to download from
        -w  warning threshold
        -c  critical threshold
        -v  Verbose
GLOUBIBOULGA
    exit $STATE_UNKNOWN
    }


#---------------------
# Retrieve and get weight of a specified web page in human-readable format
# ARGUMENTS :
#   arg1 (STRING) : URL of page to get
#   arg2 (STRING) : comma-separated list of domains to download from. Example : "static.example.com,www2.example.com"
# RETURN    : void
#---------------------
function getPage() {
    tmpFileRoot="/tmp/pageWeight.$$"
    tmpFile1="$tmpFileRoot.1"
    tmpFile2="$tmpFileRoot.2"

    [ -z "$2" ] && domainsOption='' || domainsOption="-H -D $2"

    wget -U "Internet Exploiter" -nv -np -p $domainsOption --delete-after "$1" &> $tmpFile1

    tail -n 1 $tmpFile1 > $tmpFile2
#    nbFiles=$(cut -d " " -f 2 $tmpFile2)
    weight=$(cut -d " " -f 4 $tmpFile2)
    rm $tmpFile1 $tmpFile2
#    echo "nbFiles=$nbFiles;weight=$weight"
    echo "$weight"
    }


########################################## ##########################################################
# CONFIG
########################################## ##########################################################
OPT_VERBOSE=0

exitCode=$STATE_OK
pluginOutput='Check page weight '
pluginPerfdata=''


########################################## ##########################################################
# USER INPUT VALIDATION
########################################## ##########################################################
while getopts 'h:u:d:w:c:v' option;do # http://man.cx/getopts
    case $option in
        h)
            exitShowHelp
            ;;
        u)
            OPT_URL=$OPTARG
            ;;
        d)
            OPT_DOMAINS=$OPTARG
            ;;
        w)
            OPT_WARNING=$OPTARG
            ;;
        c)
            OPT_CRITICAL=$OPTARG
            ;;
        v)
            OPT_VERBOSE=1
            ;;
        ?)
            exitShowHelp
            exit
            ;;
     esac
done

checkPluginParameter "$OPT_WARNING"  'warning (-w)'  '^[0-9]+(\.[0-9]+)?[BKMGT]?$'
checkPluginParameter "$OPT_CRITICAL" 'critical (-c)' '^[0-9]+(\.[0-9]+)?[BKMGT]?$'
checkPluginParameter "$OPT_URL"      'URL : -u'      '^http://.*'

# TODO : check URL can be fetched by wget (?)

warningThresholdBytes=$(convertToBytes $OPT_WARNING)
criticalThresholdBytes=$(convertToBytes $OPT_CRITICAL)

checkWarningIsLessThanCritical $warningThresholdBytes $criticalThresholdBytes

[ $OPT_VERBOSE -eq 1 ] && echo "[DEBUG] Options :
    OPT_URL         : $OPT_URL
    OPT_WARNING     : $OPT_WARNING ($warningThresholdBytes bytes)
    OPT_CRITICAL    : $OPT_CRITICAL ($criticalThresholdBytes bytes)
    OPT_VERBOSE     : $OPT_VERBOSE"


########################################## ##########################################################
# GETTING METRICS
########################################## ##########################################################

humanReadablePageWeight=$(getPage "$OPT_URL" "$OPT_DOMAINS")
pageWeightBytes=$(convertToBytes $humanReadablePageWeight)

[ $OPT_VERBOSE -eq 1 ] && echo "Page weight = $pageWeightBytes B ($humanReadablePageWeight)"


########################################## ##########################################################
# OUTPUT STATUS + PERFDATA
########################################## ##########################################################

if [ $warningThresholdBytes -eq 0 ] && [ $criticalThresholdBytes -eq 0 ] ;then
    exitCode=$STATE_OK
    pluginOutput=$pluginOutput"$okNoWarnString : Page weight = $humanReadablePageWeight"
elif [ $pageWeightBytes -lt $warningThresholdBytes ];then
    exitCode=$STATE_OK
    pluginOutput=$pluginOutput"OK : Page weight ($humanReadablePageWeight) < $OPT_WARNING"
elif [ $pageWeightBytes -ge $warningThresholdBytes ] && [ $pageWeightBytes -lt $criticalThresholdBytes ] ;then
    exitCode=$STATE_WARNING
    pluginOutput=$pluginOutput"WARNING : $OPT_WARNING <= Page weight ($humanReadablePageWeight) < $OPT_CRITICAL"
elif [ $pageWeightBytes -ge $criticalThresholdBytes ];then
    exitCode=$STATE_CRITICAL
    pluginOutput=$pluginOutput"CRITICAL : Page weight ($humanReadablePageWeight) >= $OPT_CRITICAL"
fi

pluginPerfdata="pageWeight=${pageWeightBytes}B;$warningThresholdBytes;$criticalThresholdBytes"
exitPlugin "$pluginOutput" "$pluginPerfdata" $exitCode

# perfdata format :
#    'label'=value[UOM];[warn];[crit];[min];[max]
# source : http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201


########################################## ##########################################################
# the end!
########################################## ##########################################################
