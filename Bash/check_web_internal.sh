#!/bin/bash

######################################### check_web_internal.sh #####################################
# FUNCTION :    Check a specific webpage from a specific webserver to make sure the website is OK
#               on all the servers of an (Apache|Lighttpd|Nginx|other) cluster.
#
# AUTHOR :      Matthieu FOURNET (matthieu.fournet@orange.com)
# LICENSE :     GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :       1. This plugin uses the HTTP "host" header to query the specified web server, but
#                  some web proxies can be configured to forbid this.
#               2. Websites can be configured to respond according to the user-agent querying them
#                  (most of the time by sending an HTTP 403 error code). This is why a custom
#                  user-agent is used in this plugin (see the "wget -U" option below)
#
# COMMAND LINE :
#               check_web_internal.sh -H "<siteName>" -s "<webServer>" -p "<webPage>" -m "<keyword>"
#               check_web_internal.sh -H "www.google.fr" -s "74.125.232.151" -p "/" -m "Search"
#
# VERSION :     20130501
########################################## ##########################################################

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
        Check a specific webpage from a specific webserver to make sure the website is OK
        on all the servers of an (Apache|Lighttpd|Nginx|other) cluster.

    USAGE:
        $0 -H "<HTTP host header>" -s "<HTTP server>" -p "<page>" -m "<string to find on page>"

    EXAMPLE:
        $0  -H "www.google.fr" -s "74.125.232.151" -p "/" -m "Search"

    OPTIONS:
        -h  Show this help
        -H  HTTP host header to send to the webserver
        -p  Page to be checked
        -s  Web server to query
        -m  String to search on the requested page
        -v  Verbose
GLOUBIBOULGA
    exit $STATE_UNKNOWN
    }


#---------------------
# Show the perfdata, return the exit code and leave script
# ARGUMENTS :
#   arg1 (STRING) : output message
#   arg2 (STRING) : output perfdata
#   arg3 (INT)    : exit code
#
# RETURN : void
#---------------------
function exitPlugin() {
    outputMessage=$1;
    outputPerfdata=$2;
    exitCode=$3;

    echo "$1|$2" # i.e. : "outputMessage|outputPerfdata"
    exit $exitCode
    }


#---------------------
# Get a page from the given webserver using HTTP headers
# ARGUMENTS :
#   arg1 (STRING) : HTTP host header
#   arg2 (STRING) : webserver
#   arg3 (STRING) : webpage
#
# RETURN : page content (string)
#---------------------
function getPage() {
    pageContent=$(wget -q -O - -U 'Internet Exploiter' --header="Host: $1" http://$2/$3)
    echo $pageContent
    }


#---------------------
# Search a string (needle) within another string (haystack) and return found/not found as a boolean
# ARGUMENTS :
#   arg1 (STRING) : needle to search for
#   arg2 (STRING) : haystack to search into
#
# RETURN : "needle was found in haystack" (boolean)
#---------------------
function stringIsFound() {
    nbMatchingLines=$(echo "$2" | grep -c "$1")
    [ $nbMatchingLines -eq 0 ] && isFound=false || isFound=true
    echo $isFound
    }

########################################## ##########################################################
# /FUNCTIONS
# CONFIG
########################################## ##########################################################
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4

OPT_VERBOSE=0

exitCode=$STATE_OK
pluginOutput='Check web internal '
pluginPerfdata=''


########################################## ##########################################################
# /CONFIG
# UNIT TESTING (uncomment to run tests)
########################################## ##########################################################

#echo -n 'Test 1 (Should find the expected string) : '
#[ $(stringIsFound "test" "don't panic : this is a test") ] && echo 'OK' || echo 'KO'

#echo -n 'Test 2 (Should NOT find the UNEXPECTED string) : '
#[ $(stringIsFound "hello" "don't panic : this is a test") ] && echo 'KO' || echo 'OK'

#echo -n 'Test 3 (Testing exit plugin) : '
#exitPlugin "(Output message) expected exit code : 0" "PerfData" $STATE_OK
#exitPlugin "(Output message) expected exit code : 1" "PerfData" $STATE_WARNING
#exitPlugin "(Output message) expected exit code : 2" "PerfData" $STATE_CRITICAL
#exitPlugin "(Output message) expected exit code : 3" "PerfData" $STATE_UNKNOWN

#exit 42
########################################## ##########################################################
# /UNIT TESTING
# USER INPUT VALIDATION
########################################## ##########################################################
while getopts 'h:H:m:p:s:v' option;do    # http://man.cx/getopts
    case $option in
        h)
            exitShowHelp
            ;;
        H)
            OPT_HOSTHEADER=$OPTARG
            ;;
        m)
            OPT_MATCHSTRING=$OPTARG
            ;;
        p)
            OPT_WEBPAGE=$OPTARG
            ;;
        s)
            OPT_WEBSERVER=$OPTARG
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

if [ $OPT_VERBOSE -eq 1 ]; then
    echo "[DEBUG] Options :
    OPT_HOSTHEADER  : $OPT_HOSTHEADER
    OPT_MATCHSTRING : $OPT_MATCHSTRING
    OPT_WEBPAGE     : $OPT_WEBPAGE
    OPT_WEBSERVER   : $OPT_WEBSERVER
    OPT_VERBOSE     : $OPT_VERBOSE"
fi


########################################## ##########################################################
# GETTING METRICS
########################################## ##########################################################

pageContent=$(getPage $OPT_HOSTHEADER $OPT_WEBSERVER $OPT_WEBPAGE)
#echo $pageContent


########################################## ##########################################################
# OUTPUT STATUS + PERFDATA
########################################## ##########################################################
blablaString=" : string '$OPT_MATCHSTRING' was "
pageString="found on page '$OPT_WEBPAGE' from the webserver '$OPT_WEBSERVER'."

if $(stringIsFound "$OPT_MATCHSTRING" "$pageContent");then
    outputMessage=$pluginOutput'OK'$blablaString$pageString
    exitCode=$STATE_OK
else
    outputMessage=$pluginOutput'CRITICAL'$blablaString$'NOT '$pageString
    exitCode=$STATE_CRITICAL
fi

exitPlugin "$outputMessage" "$pluginPerfdata" $exitCode

# perfdata format :
#    'label'=value[UOM];[warn];[crit];[min];[max]
# source : http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201


########################################## ##########################################################
# the end!
########################################## ##########################################################
