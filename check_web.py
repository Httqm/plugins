#!/usr/bin/env python

######################################### check_web.py ##############################################
# FUNCTION :	
#
# AUTHOR :	Matthieu FOURNET (matthieu.fournet@orange.com)
# LICENSE :	GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :	1.
#
# COMMAND LINE :
#	clear;./check_web.py --url=http://www.truc.biz --httpHeader="Host: www.bidule.org" --matchString="un mot" -w 2500 -c 4000 --debug
#
# TODO :
#		-
########################################## ##########################################################

import urllib                          # http://docs.python.org/library/httplib.htm
# http://docs.python.org/library/urllib.html?highlight=urllib
#from optparse import OptionParser       
import argparse # http://docs.python.org/library/argparse.html#module-argparse 
# not yet available in Deb packages for python3 :-(




########################################## ##########################################################
# FUNCTIONS
########################################## ##########################################################

########################################## ##########################################################
# /FUNCTIONS
# CONFIG
########################################## ##########################################################
nagiosPluginExitCode = {
    0: 'OK',
    1: 'WARNING',
    2: 'CRITICAL',
    3: 'UNKNOWN'
    }


########################################## ##########################################################
# /CONFIG
# main()
########################################## ##########################################################

# Declare/load/check args
myParser = argparse.ArgumentParser(description = 'Check a web page')

myParser.add_argument('-u', '--url',            type = str, dest = 'url',           required = True,    help = 'URL of page to check')
myParser.add_argument('-H', '--httpHeader',     type = str, dest = 'httpHeader',    required = False,   help = 'HTTP host header (optional)')
myParser.add_argument('-m', '--matchString',    type = str, dest = 'matchString',   required = True,    help = 'String to search on page')
myParser.add_argument('-w', '--warning',        type = int, dest = 'warning',       required = True,    help = 'warning threshold in ms')
myParser.add_argument('-c', '--critical',       type = int, dest = 'critical',      required = True,    help = 'critical threshold in ms')

#myParser.add_argument('--debug', dest = 'debug', action = 'store_const', const = False, required = False)
myParser.add_argument('--debug', action = 'store_true')

#myParser.parse_args()

args = myParser.parse_args()
print args

#print args('url')



# validate args

# enable plugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer

# send http request (get, post, cookie, ...) with optionnal header(s)

# get result + HTTP exit code

# stop timer

# if HTTP exit code is "success", search matchstring
# otherwise, exit with error message + nagios status code

# if matchstring found, report success (nagios status code) + perfdata
# otherwise, report failure + nagios status code + perfdata




########################################## ##########################################################
# /main()
# THE END !
########################################## ##########################################################
