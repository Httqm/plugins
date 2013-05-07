#!/bin/bash

######################################### Functions/MySQL.sh ########################################
# FUNCTION :	Various shell functions dedicated to MySQL.
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

#---------------------
# Identifies the MySQL client binary
#
# ARGUMENTS :
#	(none)
#
# RETURN : (STRING) Absolute path to MySQL client binary (if found. Otherwise, leave on error.)
#---------------------
getMySQLBinary() {
	export mysqlBin=$(which mysql)
	[ -z $mysqlBin ] && { exitPlugin 'No MySQL client found.' '' $STATE_UNKNOWN; }
#	echo $mysqlBin
	}


#---------------------
# Execute the given SQL query
#
# ARGUMENTS :
#	arg1 (STRING) : MySQL query
#
# RETURN :
#---------------------
executeSqlQuery() {
#	command="$mysqlBin -h \"$1\" -u \"$2\" -p\"$3\" \"$4\" -e \"$5\""
#	command="$mysqlBin -h \"$1\" -u \"$2\" -p\"$3\" -e \"$5\""
	command="$mysqlBin -h $OPT_MYSQLHOST -u $OPT_MYSQLUSER -p$OPT_MYSQLPASSWORD -e \"$1\" "
	echo $command
	$command &>/dev/null
	returnCode=$?
	echo "RETURN CODE : $returnCode"
	}


#---------------------
# Test availability of of a DB
#
# ARGUMENTS :
#	arg1 (STRING) : DB Name
#
# RETURN : (boolean) DB exists Y/N
#---------------------
dbExists() {
	$mysqlBin -h $OPT_MYSQLHOST -u $OPT_MYSQLUSER -p$OPT_MYSQLPASSWORD -e "use $1 ;" &>/dev/null
	returnCode=$?
	[ $returnCode -eq 0 ] && echo true || echo false
	}
