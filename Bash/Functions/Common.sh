#!/bin/bash

######################################### Functions/Common.sh ########################################
# FUNCTION :	Various shell functions common to all scripts.
#
# AUTHOR :		Matthieu FOURNET (matthieu.fournet@orange.com)
# LICENSE :		GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :		1. Start this script with the '-t' flag to launch unit tests
#
#
# VERSION :		20130525
#
# TODO :
########################################## ##########################################################

########################################## ##########################################################
# CONSTANTS
########################################## ##########################################################
export STATE_OK=0
export STATE_WARNING=1
export STATE_CRITICAL=2
export STATE_UNKNOWN=3
export STATE_DEPENDENT=4

########################################## ##########################################################
# FUNCTIONS
########################################## ##########################################################

#---------------------
# 
# ARGUMENTS :
#	arg1 (STRING) :	human readable file size
#
# RETURN : (INT) size in bytes
#---------------------
convertToBytes() {
	# cleaning the input data
	cleanInputString=$(echo $1 | tr ', ' '.')
	echo "|"$cleanInputString"|"
	}

#---------------------
# Show (or not) the perfdata, return the exit code and leave script
# ARGUMENTS :
#	arg1 (STRING) :	output message
#	arg2 (STRING) : output perfdata
#	arg3 (INT) : 	exit code
#
# RETURN : void
#---------------------
exitPlugin() {
	outputMessage=$1;
	outputPerfdata=$2;
	exitCode=$3;

	echo "$1|$2"	# i.e. : "outputMessage|outputPerfdata"
	exit $exitCode
	}




# TODO : format this

# Echo text messages in color.

# $1 : color
# $2 : message
# $3 : bold 0|1

# Examples :
#colorEcho red "red, normal" 0
#colorEcho red "red, bold" 1

#colorEcho green "green, normal" 0
#colorEcho green "green, bold" 1
function colorEcho() {
	bold=${3:-0}		# Defaults to "not bold", if not specified.

	declare -A colors	# required to declare an associative array
	
	colors['red']="\e[$bold;31m"
	colors['green']="\e[$bold;32m"
	colors['yellow']="\e[$bold;33m"
	colors['blue']="\e[$bold;34m"
	colors['purple']="\e[$bold;35m"
	colors['cyan']="\e[$bold;36m"
	colors['white']="\e[$bold;37m"
	colors['reset']='\e[0m'	# Reset text attributes to normal without clearing screen.

#	echo "couleur(1) : $1"
#	echo "couleur(2) : ${colors[$1]}"
#	echo "bold : $bold"

	echo -e "${colors[$1]}$2${colors['reset']}"
	}







########################################## ##########################################################
# UNIT TESTS
########################################## ##########################################################
if [ "$1" == '-t' ]
then

	echo -n 'convertToBytes '
	[ "$(convertToBytes ' 1.2M ')" == '|1.2M|' ] && colorEcho green OK || colorEcho red KO

fi