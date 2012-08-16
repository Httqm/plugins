#!/usr/bin/env python

######################################### check_web.py ##############################################
# FUNCTION :	
#
# AUTHOR :	Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :	GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :	1.
#
# COMMAND LINE :
#	clear;./check_web.py --url="http://www.perdu.com" --httpHostHeader="www.perdu.com" --matchString="un mot" -w 2500 -c 4000 --debug
#	clear;./check_web.py --url="http://origin-www.voici.fr" --httpHostHeader="www.voici.fr" --matchString="un mot" -w 2500 -c 4000 --debug
#
# TODO :
#		-
########################################## ##########################################################

#import urllib                          # http://docs.python.org/library/httplib.htm
import httplib
# http://docs.python.org/library/urllib.html?highlight=urllib
import argparse

from modules import debug

debug = debug.Debug()

#debug.die({'exitMessage': 'argl, je meurs, je meurs de facon... tragique!'})
########################################## ##########################################################
# CLASSES
########################################## ##########################################################

import re

class Url(object):

    def __init__(self, params):
        self._full = params['full']
        self._clean()


    def _clean(self):
        # http://docs.python.org/library/stdtypes.html#str.rstrip
        self._full = self._full.lstrip().rstrip()
        print 'CLEAN URL : "' + self._full + '"'


    def getFullUrl(self):
        return self._full


    def getQueryUrl(self):
        import string
        tmp = string.replace(self._full, 'http://' + self.getHostName(), '')
        return tmp if len(tmp) else '/'


    def getHostName(self):
        match = re.search('^http://([^:/]*)(:|/)?.*$', self._full)   # TODO : should start with 'http....', no leading space allowed
        # http://docs.python.org/howto/regex#performing-matches
        if match:
            return match.group(1)
        else:
            return self._full



########################################## ##########################################################
# /CLASSES
# FUNCTIONS
########################################## ##########################################################
def lengthOfLongestKey(aDict):
    length = 0
    for key in aDict:
        keyLength   = len(str(key))
        if keyLength > length:
            length = keyLength
    return length


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

# http://docs.python.org/library/argparse.html#the-add-argument-method
myParser.add_argument('-u', '--url',            type = str, dest = 'url',           required = True,    help = 'URL of page to check with leading "http://"')

myParser.add_argument('-p', '--httpPort',       type = int, dest = 'httpPort',      required = False,   help = 'HTTP port (optional. Defaults to 80)', default = 80)


myParser.add_argument('-m', '--matchString',    type = str, dest = 'matchString',   required = True,    help = 'String to search on page')
myParser.add_argument('-w', '--warning',        type = int, dest = 'warning',       required = True,    help = 'warning threshold in ms')
myParser.add_argument('-c', '--critical',       type = int, dest = 'critical',      required = True,    help = 'critical threshold in ms')
myParser.add_argument('-H', '--httpHostHeader',     type = str, dest = 'httpHostHeader',    required = False,   help = 'HTTP host header (optional)')
myParser.add_argument(      '--debug',  required = False, action = 'store_true')


args    = myParser.parse_args()
theArgs = {
    'url'           : args.url,
    'matchString'   : args.matchString,
    'warning'       : args.warning,
    'critical'      : args.critical,
    'httpHostHeader'    : args.httpHostHeader,
    'httpPort'      : args.httpPort,
    'debug'         : args.debug
    }


# TODO : refuse the URL arg if it doesn't start EXACTLY with "http://"
# TODO : no port number allowed in URL
url = Url({
        'full' : args.url
        })



debug.show(
    'URL (full) = ' + url.getFullUrl() + "\n" \
    'URL (query) = ' + url.getQueryUrl() + "\n" \
    'HOSTNAME = ' + url.getHostName() + "\n" \
    'HOST HEADER = ' + args.httpHostHeader + "\n" \
    'HTTP PORT = ' + str(args.httpPort)
    )

debug.die({'exitMessage': 'argl, je meurs, je meurs de facon... tragique!'})

length = lengthOfLongestKey(theArgs)
for key in theArgs:
    print str(key).rjust(length + 1) + ': ' + str(theArgs[key])





# enable plugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer






# send http request (get, post, cookie, ...) with optionnal header(s)
# http://docs.python.org/library/httplib.html#httplib.HTTPConnection
#httpConnection = httplib.HTTPConnection('www.perdu.com', 80, timeout=10)
httpConnection = httplib.HTTPConnection(
    url.getHostName(),
    args.httpPort,
    timeout = 10
    )
#TODO : host must be HTTP (no httpS) and have no leading "http://"


# example : http://www.dev-explorer.com/articles/using-python-httplib
httpConnection.request('GET', '/', {}, {'Host': args.httpHostHeader})

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
