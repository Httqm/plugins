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
#   clear;./check_web.py --url="http://www.perdu.com" --httpHostHeader="www.perdu.com" --matchString="un mot" -w 2500 -c 4000 --debug
#   clear;./check_web.py --url="http://origin-www.voici.fr" --httpHostHeader="www.voici.fr" --matchString="un mot" -w 2500 -c 4000 --debug
#   clear;./check_web.py --url="http://origin-www.voici.fr" --httpHostHeader="www.voici.fr" --httpMethod=get --matchString="un mot" -w 2500 -c 4000 --debug
#
# TODO :
#		-
########################################## ##########################################################

#import urllib  # http://docs.python.org/library/urllib.html?highlight=urllib
import httplib  # http://docs.python.org/library/httplib.htm

from modules import debug


########################################## ##########################################################
# CLASSES
########################################## ##########################################################

import re

class nagiosPlugin(object):

    def __init__(self, params):
        self._objDebug  = params['objDebug']
        self._exitCodes = {
            0: 'OK',
            1: 'WARNING',
            2: 'CRITICAL',
            3: 'UNKNOWN'
            }
#        self._debugIsEnabled = False

        import argparse
        self._argParser = argparse.ArgumentParser(description = 'Check a web page') # TODO : this is not GENERIC !
        self._argDict   = {}


    def addArg(self, argData):
        # http://docs.python.org/library/argparse.html#the-add-argument-method
        self._argParser.add_argument(
            '-'     + argData['shortOption'],
            '--'    + argData['longOption'],
            type        = str,  # Even warn / crit can be strings when defining ranges : "50:100"
            dest        = argData['longOption'],
            required    = argData['required'],
            default     = argData['default'],
            help        = argData['help']
            )
        self._argDict[argData['longOption']] = {
            'value' : 0,
            'rule'  : argData['rule']
            }


    def addArgDebug(self):
        self._argParser.add_argument(
            '--debug',
            required    = False,
            action      = 'store_true',
            help        = 'Toggle debug messages'
            )
        self._argDict['debug'] = {}


    def readArgs(self):
        self._args = self._argParser.parse_args()
        for argName in self._argDict:
            self._argDict[argName]['value'] = getattr(self._args, argName)
        self._detectDebugValue()
        self._validateArgs()


    def _detectDebugValue(self):
        if self._argDict['debug']['value']:
            self._objDebug.enable(True)
            self._objDebug.show('DEBUG IS ENABLED!')


    def _validateArgs(self):
        self._objDebug.show(self._argDict)
        import re
        for argName in self._argDict:
            if argName == 'debug' or not len(self._argDict[argName]['rule']) : # The debug arg has a boolean value that doesn't fit the regexp search, and has no 'rule'. TODO : fix this if possible
                continue
            message = '(for "' + argName + '")' \
                + ' RULE : "' + self._argDict[argName]['rule'] \
                + '", VALUE : "' + str(self._argDict[argName]['value']) + '"'
            if re.search('^' + self._argDict[argName]['rule'] + '$', str(self._argDict[argName]['value'])):
                matchMessage = 'MATCHED :'
            else:
                matchMessage = 'NO MATCH :-('
                self._objDebug.die({'exitMessage': 'Invalid value "' + str(self._argDict[argName]['value']) + '" for argument "' + argName + '".'})
            self._objDebug.show(matchMessage + ' ' + message)


    def showArgs(self):
        util    = utility()
        length  = util.lengthOfLongestKey(self._argDict)
        """
        for key in self._argList:
            print str(key).rjust(length + 1) + ': ' + str(getattr(self._args, key))
        print 'SHOWARGS'
        print length
        """
        for argName in self._argDict:
            print str(argName).rjust(length + 1) + ': ' + str(self._argDict[argName]['value'])
#            print 'RULE : ' + self._argDict[argName]['rule']


    def getArgValue(self, argName):
        return getattr(self._args, argName)


    def _checkArgs(self):
        pass


    def addPerfData(self):
        pass


    def exit(self):
        pass



class check_web(nagiosPlugin):

    def getPage(self):
        pass


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


class utility(object):

    def lengthOfLongestKey(self, aDict):
        length = 0
        for key in aDict:
            keyLength   = len(str(key))
            if keyLength > length:
                length = keyLength
        return length


########################################## ##########################################################
# /CLASSES
# CONFIG
########################################## ##########################################################


########################################## ##########################################################
# /CONFIG
# main()
########################################## ##########################################################

objDebug = debug.Debug()

plugin = check_web({
    'objDebug': objDebug
    })

plugin.addArg({
    'shortOption'   : 'u',
    'longOption'    : 'url',
    'required'      : True,
    'default'       : None,
    'help'          : 'URL of page to check with leading "http://"',
    'rule'          : 'http://.*'
    })

plugin.addArg({
    'shortOption'   : 'p',
    'longOption'    : 'httpPort',
    'required'      : False,
    'default'       : 80,
    'help'          : 'HTTP port (optional. Defaults to 80)',
    'rule'          : '\d+'
    })

plugin.addArg({
    'shortOption'   : 'M',
    'longOption'    : 'httpMethod',
    'required'      : False,
    'default'       : 'GET',
    'help'          : 'HTTP method (optional. Defaults to GET)',
    'rule'          : '(GET|POST|HEAD)'
    })

plugin.addArg({
    'shortOption'   : 'm',
    'longOption'    : 'matchString',
    'required'      : True,
    'default'       : None,
    'help'          : 'String to search on page',
    'rule'          : '[\w ]+'
    })

plugin.addArg({
    'shortOption'   : 'w',
    'longOption'    : 'warning',
    'required'      : True,
    'default'       : None,
    'help'          : 'warning threshold in ms',
    'rule'          : '(\d+:?|:\d+|\d+:\d+)'
    })

plugin.addArg({
    'shortOption'   : 'c',
    'longOption'    : 'critical',
    'required'      : True,
    'default'       : None,
    'help'          : 'critical threshold in ms',
    'rule'          : ''
    })

plugin.addArg({
    'shortOption'   : 'H',
    'longOption'    : 'httpHostHeader',
    'required'      : True,
    'default'       : None,
    'help'          : 'HTTP host header (optional)',
    'rule'          : ''
    })

plugin.addArgDebug()

plugin.readArgs()
plugin.showArgs()



print 'url = ' + plugin.getArgValue('url')


# TODO : refuse the URL arg if it doesn't start EXACTLY with "http://"
# TODO : no port number allowed in URL
url = Url({
    'full' : plugin.getArgValue('url')
    })

objDebug.die({'exitMessage': 'ARGL !'})




# enable plugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer






# send http request (get, post, cookie, ...) with optionnal header(s)
# http://docs.python.org/library/httplib.html#httplib.HTTPConnection
#httpConnection = httplib.HTTPConnection('www.perdu.com', 80, timeout=10)
httpConnection = httplib.HTTPConnection(
    url.getHostName(),
    plugin.getArgValue('httpPort'),
    timeout = 10
    )
#TODO : host must be HTTP (no httpS) and have no leading "http://"


# example : http://www.dev-explorer.com/articles/using-python-httplib
#httpConnection.request('GET', '/', {}, {'Host': args.httpHostHeader})
httpConnection.request(
#    'POST',
    plugin.getArgValue('httpMethod'),
    '/',
    {},
    {'Host': plugin.getArgValue('httpHostHeader')}
    )


httpResponse = httpConnection.getresponse()
# returns an HTTPResponse object :
#   http://docs.python.org/library/httplib.html#httplib.HTTPResponse
#   http://docs.python.org/library/httplib.html#httpresponse-objects

print httpResponse.read()








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
