#!/bin/bash

######################################### Functions/Common.sh ########################################
# FUNCTION :    Various shell functions common to all scripts.
#
# AUTHOR :      Matthieu FOURNET (matthieu.fournet@orange.com)
# LICENSE :     GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :       1. Start this script with the '-t' flag to launch unit tests
#
# VERSION :     20130604
########################################## ##########################################################

########################################## ##########################################################
# CONSTANTS
########################################## ##########################################################
export STATE_OK=0
export STATE_WARNING=1
export STATE_CRITICAL=2
export STATE_UNKNOWN=3
export STATE_DEPENDENT=4

export okNoWarnString='NO WARN'

########################################## ##########################################################
# FUNCTIONS
########################################## ##########################################################


#---------------------
# Perform an arithmetic round on the input value into an integer.
# ARGUMENTS :
#   arg1 (FLOAT) : number to be rounded
#
# RETURN : (INT) Rounded number
#---------------------
function round() {
    # Source : http://www.alecjacobson.com/weblog/?p=256
    # The "+0.5" hack is there because "bc" 'floors' but doesn't 'round'
    echo "($1+0.5)/1" | bc
    }


#---------------------
# Make sure the warning threshold is effectively < the critical threshold.
# ARGUMENTS :
#   arg1 (FLOAT) : warning threshold
#   arg2 (FLOAT) : critical threshold
#
# RETURN : void (exit on error)
#---------------------
function checkWarningIsLessThanCritical() {
    [ $1 -ge $2 ] && {
        echo;echo "    Warning must be < than critical.";echo
        exitShowHelp
        }
    }


#---------------------
# Check a plugin parameter against a validating RegExp.
# ARGUMENTS :
#   arg1 (STRING) : parameter value.
#   arg2 (STRING) : parameter 'display name' (for error message only).
#   arg3 (STRING) : parameter validation RegEx.
#
# RETURN : void (exit on error)
#---------------------
function checkPluginParameter() {
    [[ ! "$1" =~ $3 ]] && {
        echo;echo "    Wrong value for parameter $2 : '$1'.";echo
        exitShowHelp
        }
    }


#---------------------
# Extract a single field identified by its number from a line.
# ARGUMENTS :
#   arg1 (STRING) : line. Must be protected from inner spaces : use ""
#   arg2 (INT) : field numbername of file to process
#
# RETURN : (STRING) field value
#---------------------
function getFieldFromLine() {
    echo $1 | cut -d ' ' -f $2
    }


#---------------------
# Remove the first line a of string.
# ARGUMENTS :
#   arg1 (STRING) : name of file to process
#
# RETURN : void (file is overwritten)
#---------------------
function removeFirstLineOfFile() {
    sed -i '1d' $1
    }


#---------------------
# Search a string (needle) within another string (haystack) and return found/not found as a boolean
# ARGUMENTS :
#   arg1 (STRING) : needle to search for
#   arg2 (STRING) : haystack to search into
#
# RETURN : (BOOLEAN) "needle was found in haystack"
#---------------------
function stringIsFound() {
    nbMatchingLines=$(echo "$2" | grep -c "$1")
    [ $nbMatchingLines -eq 0 ] && isFound=false || isFound=true
    echo $isFound
    }


#---------------------
# Convert a file size given as a string (12K, 23KB, 1.5GB, ...) into bytes.
# ARGUMENTS :
#   arg1 (STRING) : human readable file size
#
# RETURN : (INT) size in bytes
# NOTE : There must be no space between the number and the unit letter.
#---------------------
export INVALID_SIZE_STRING='Invalid size provided.'

function convertToBytes() {
    # cleaning the input data (locales, ...)
    cleanInputString=$(echo $1 | tr ',' '.')

    # checking the input string is a file size
    [[ ! "$cleanInputString" =~ ^[0-9]+(\.[0-9]+)?[KMGT]?B?$ ]] && { echo "$INVALID_SIZE_STRING";return; }

    # converting
    cleanInputString=$(echo $cleanInputString | sed 's/B//')
    [[ "$cleanInputString" =~ [0-9]$ ]] && cleanInputString="${cleanInputString}B"  # to avoid special case hereafter

    [[ "$cleanInputString" =~ B$ ]] && power=0
    [[ "$cleanInputString" =~ K$ ]] && power=1
    [[ "$cleanInputString" =~ M$ ]] && power=2
    [[ "$cleanInputString" =~ G$ ]] && power=3
    [[ "$cleanInputString" =~ T$ ]] && power=4

    nbBytes=$(echo $cleanInputString | sed "s/[BKMGT]/*\(1024^$power\)/" | bc)  # This may be a float, hence the 'round' below.
    echo $(round $nbBytes)
    }


#---------------------
# Show (or not) the perfdata, return the exit code and leave script
# ARGUMENTS :
#   arg1 (STRING) : output message
#   arg2 (STRING) : output perfdata
#   arg3 (INT) :    exit code
#
# RETURN : void
#---------------------
function exitPlugin() {
    outputMessage=$1;
    outputPerfdata=$2;
    exitCode=$3;

    echo "$1|$2"    # i.e. : "outputMessage|outputPerfdata"
    exit $exitCode
    }


#---------------------
# Echo text messages in color.
# ARGUMENTS :
#    arg1 (STRING) : color
#    arg2 (STRING) : message
#    arg3 (INT) :    bold 0|1
#
# RETURN : void
# EXAMPLES :
#    colorEcho red "red, normal" 0
#    colorEcho red "red, bold" 1
#---------------------
function colorEcho() {
    bold=${3:-0}    # Defaults to "not bold", if not specified.

    declare -A colors   # required to declare an associative array

    colors['red']="\e[$bold;31m"
    colors['green']="\e[$bold;32m"
    colors['yellow']="\e[$bold;33m"
    colors['blue']="\e[$bold;34m"
    colors['purple']="\e[$bold;35m"
    colors['cyan']="\e[$bold;36m"
    colors['white']="\e[$bold;37m"
    colors['reset']='\e[0m' # Reset text attributes to normal without clearing screen.

    echo -e "${colors[$1]}$2${colors['reset']}"
    }


########################################## ##########################################################
# UNIT TESTS
########################################## ##########################################################
if [ "$1" == '-t' ]
then

    ###################################### ##########################################################
    # convertToBytes
    ###################################### ##########################################################
    declare -A testData # declares an associative array

    testData['test']="$INVALID_SIZE_STRING"
    testData['3X']="$INVALID_SIZE_STRING"
    testData['1,,2M']="$INVALID_SIZE_STRING"
    testData['1.2M']='1258291'
    testData['42']='42'
    testData['12.34']='12'
    testData['42B']='42'
    testData['42K']='43008'
    testData['42KB']='43008'
    testData['42.4242KB']='43442'
    testData['42M']='44040192'
    testData['42MB']='44040192'
    testData['42G']='45097156608'
    testData['42GB']='45097156608'
    testData['12.34GB']='13249974108'

    for i in "${!testData[@]}"; do
        testString="$i"
        expectedResult="${testData[$i]}"
        echo -n "convertToBytes ('$testString') ... "
        [ "$(convertToBytes $testString)" == "$expectedResult" ] && colorEcho green OK 1 || colorEcho red KO 1
#        echo 'DEBUG : '$testString" ==> $(convertToBytes $testString)";echo
    done
    unset testData
    ###################################### ##########################################################
    # /convertToBytes
    ###################################### ##########################################################

    ###################################### ##########################################################
    # round
    ###################################### ##########################################################
    declare -A testData # declares an associative array

    testData['0']=0
    testData['1']=1
    testData['1.4']=1
    testData['1.6']=2
    testData['123456789.123456789']=123456789
    testData['1.50000000000']=2

    for i in "${!testData[@]}"; do
        testValue="$i"
        expectedResult="${testData[$i]}"
        echo -n "round ('$testValue') ... "
        [ "$(round $testValue)" == "$expectedResult" ] && colorEcho green OK 1 || colorEcho red KO 1
#        echo 'DEBUG : '$testValue" ==> $(round $testValue)";echo
    done
    unset testData
    ###################################### ##########################################################
    # /round
    ###################################### ##########################################################

fi
