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
#	clear;./check_web.py --url=http://www.perdu.com --httpHostHeader="Host: www.perdu.com" --matchString="un mot" -w 2500 -c 4000 --debug
#	clear;./check_web.py --url=http://www.google.fr --httpHostHeader="Host: www.perdu.com" --matchString="un mot" -w 2500 -c 4000 --debug
#
# TODO :
#		-
########################################## ##########################################################

#import urllib                          # http://docs.python.org/library/httplib.htm
import httplib
# http://docs.python.org/library/urllib.html?highlight=urllib
import argparse



########################################## ##########################################################
# FUNCTIONS
########################################## ##########################################################
def lengthOfLongestKey(aDict):
    length = 0
    for key in aDict:
        keyLength   = len(str(key))
        if keyLength > length:
            length = keyLength
    return length


def getHostNameFromUrl(url):
    import re
    match = re.search('^.*http://([^/]*)/?.*$', url)
    # http://docs.python.org/howto/regex#performing-matches
    if match:
        return match.group(1)
    else:
        return url


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




# Declare/load/validate args
myParser = argparse.ArgumentParser(description = 'Check a web page')

myParser.add_argument('-u', '--url',            type = str, dest = 'url',               required = True,    help = 'URL of page to check with leading "http://"')
myParser.add_argument('-m', '--matchString',    type = str, dest = 'matchString',       required = True,    help = 'String to search on page')
myParser.add_argument('-w', '--warning',        type = int, dest = 'warning',           required = True,    help = 'warning threshold in ms')
myParser.add_argument('-c', '--critical',       type = int, dest = 'critical',          required = True,    help = 'critical threshold in ms')
myParser.add_argument('-H', '--httpHostHeader', type = str, dest = 'httpHostHeader',    required = False,   help = 'HTTP host header (optional)')
myParser.add_argument(      '--debug',  required = False, action = 'store_true')


args    = myParser.parse_args()
theArgs = {
    'url'               : args.url,
    'matchString'       : args.matchString,
    'warning'           : args.warning,
    'critical'          : args.critical,
    'httpHostHeader'    : args.httpHostHeader,
    'debug'             : args.debug
    }


length = lengthOfLongestKey(theArgs)
for key in theArgs:
    print str(key).rjust(length + 1) + ': ' + str(theArgs[key])





# enable plugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer


print args.url
print getHostNameFromUrl(args.url)

# send http request (get, post, cookie, ...) with optionnal header(s)
# http://docs.python.org/library/httplib.html#httplib.HTTPConnection
#httpConnection = httplib.HTTPConnection('www.perdu.com', 80, timeout=10)
httpConnection = httplib.HTTPConnection(
    getHostNameFromUrl(args.url),
    80,
    timeout = 10
    )
#TODO : host must be HTTP (no httpS) and have no leading "http://"

#httpConnection.request('get', 'www.google.be', '', '')
#httpConnection.request('GET', 'http://www.perdu.com')
httpConnection.request('GET', args.url)

truc=httpConnection.getresponse()
# returns an HTTPResponse object :
#   http://docs.python.org/library/httplib.html#httplib.HTTPResponse
#   http://docs.python.org/library/httplib.html#httpresponse-objects
print truc.read()





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
