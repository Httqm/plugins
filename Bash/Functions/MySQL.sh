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

########################################## ##########################################################
# FUNCTIONS
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
	}


#---------------------
# Execute the given SQL query
#
# ARGUMENTS :
#	arg1 (STRING) : MySQL query
#	arg2 (STRING) : results file
#
# RETURN :
#---------------------
executeSqlQuery() {
	$mysqlBin -h $OPT_MYSQLHOST -u $OPT_MYSQLUSER -p$OPT_MYSQLPASSWORD -e "$1" > $2
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


#---------------------
# Leave script if the specified DB doesn't exist
#
# ARGUMENTS : (none)
#
# RETURN : (none)
#---------------------
leaveScriptIfDbNotFound() {
	if ! $(dbExists "$OPT_MYSQLDBNAME"); then
		{ exitPlugin "Database '$OPT_MYSQLDBNAME' not found on MySQL server '$OPT_MYSQLHOST'." '' $STATE_UNKNOWN; echo 'does not exist'; }
	fi
	}


########################################## ##########################################################
# main()
########################################## ##########################################################
getMySQLBinary
