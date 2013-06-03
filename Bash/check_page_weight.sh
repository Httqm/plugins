#!/bin/bash

######################################### check_page_weight.sh ######################################
# FUNCTION :    Measure the weight of the given webpage, including its HTML source code and linked
#               files (CSS, JS, images), and warn accordingly.
#
# AUTHOR :      Matthieu FOURNET (matthieu.fournet@orange.com)
# LICENSE :     GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :       1.
#
# COMMAND LINE :
#               check_page_weight.sh -u "<URL of page to check>" -w "<warn>" -c "<crit>"
#               check_page_weight.sh -u "http://www.google.com" -w 50KB -c 100KB -v
#
# VERSION :     20130603
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
        $0 -u "<URL of page to check>" -w "<warn>" -c "<crit>"

    EXAMPLE:
        $0 -u "http://www.google.fr" -w 50K -c 100K -v

    OPTIONS:
        -h  Show this help
        -u  URL of page to check
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
# RETURN    : void
#---------------------
function getPage() {
    tmpFileRoot="/tmp/pageWeight.$$"
    tmpFile1="$tmpFileRoot.1"
    tmpFile2="$tmpFileRoot.2"
    wget -U "Internet Exploiter" -nv -np -p --delete-after "$1" &> $tmpFile1
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
while getopts 'h:u:w:c:v' option;do # http://man.cx/getopts
    case $option in
        h)
            exitShowHelp
            ;;
        u)
            OPT_URL=$OPTARG
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

checkPluginParameter "$OPT_WARNING" 'warning (-w)' '^[0-9]+(\.[0-9]+)?[BKMGT]?$'
checkPluginParameter "$OPT_CRITICAL" 'critical (-c)' '^[0-9]+(\.[0-9]+)?[BKMGT]?$'
checkPluginParameter "$OPT_URL" 'URL : -u' '^http://.*'

# TODO : check URL can be fetched by wget (?)

warningThresholdBytes=$(convertToBytes $OPT_WARNING)
criticalThresholdBytes=$(convertToBytes $OPT_CRITICAL)

# TODO : check warning < critical

[ $OPT_VERBOSE -eq 1 ] && echo "[DEBUG] Options :
    OPT_URL         : $OPT_URL
    OPT_WARNING     : $OPT_WARNING ($warningThresholdBytes bytes)
    OPT_CRITICAL    : $OPT_CRITICAL ($criticalThresholdBytes bytes)
    OPT_VERBOSE     : $OPT_VERBOSE"


########################################## ##########################################################
# GETTING METRICS
########################################## ##########################################################

humanReadablePageWeight=$(getPage $OPT_URL)
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

pluginPerfdata="pageWeight=${pageWeightBytes}Bytes;$warningThresholdBytes;$criticalThresholdBytes"
exitPlugin "$pluginOutput" "$pluginPerfdata" $exitCode

# perfdata format :
#    'label'=value[UOM];[warn];[crit];[min];[max]
# source : http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201


########################################## ##########################################################
# the end!
########################################## ##########################################################
