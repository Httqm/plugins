#!/bin/bash

######################################### Functions/Common.sh ########################################
# FUNCTION :	Various shell functions common to all scripts.
#
# AUTHOR :		Matthieu FOURNET (matthieu.fournet@orange.com)
# LICENSE :		GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :		1. 
#
#
# VERSION :		20130507
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
