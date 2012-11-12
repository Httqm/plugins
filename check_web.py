#!/usr/bin/env python

# check_web.py - Copyright (C) 2012 Matthieu FOURNET, fournet.matthieu@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

######################################### check_web.py ##############################################
# FUNCTION :    This plugin provides various means to check a web page :
#                - query a web page and check its content for a keyword
#                - query a web page and check its HTTP return code
#                - or both
#                - with or without using warn / crit duration thresholds on the page response time
#
# VERSION :     20121023
#
# COMMAND LINE :    (the scissors 8< mean the command continues on the next line)
#   SEARCHING MATCHSTRING ON WEB PAGE :
#       ./check_web.py --url="http://origin-www.voici.fr" --httpHostHeader="www.voici.fr" 8<
#           --httpMethod="GET" --httpStatusCode 200 --matchString="kate" -w 2500 -c 4000 --debug
#
#   PLAYING WITH EXPECTED HTTP STATUS CODES :
#       ./check_web.py --url="http://origin-www.voici.fr" --httpHostHeader="origin-www.voici.fr" 8<
#           --httpMethod="GET" --httpStatusCode 301 --matchString="bla" -w 2500 -c 4000 --debug
#
# NOTES :	1. (none so far ;-)
#
# KNOWN BUGS AND LIMITATIONS :
#               1. 
#
########################################## ##########################################################


# TODO :
# - handle case when no matchstring is provided :
#       1. no error when re.searching as it's empty
#       2. if no string is provided, it means we don't care about strings matching, just HTTP codes (?)
# ex: ./check_web.py --url="http://origin-www.voici.fr" --httpMethod="GET" --httpStatusCode 301 -w 2500 -c 4000 --debug
#
# prepare case matrix for different check types / results / exits
# /TODO


#import urllib  # http://docs.python.org/library/urllib.html?highlight=urllib
import httplib  # http://docs.python.org/library/httplib.htm
import re

from modules import CommandLine
from modules import Debug
from modules import NagiosPlugin
from modules import Url
from modules import Utility


########################################## ##########################################################
# CLASSES
########################################## ##########################################################

class check_web(NagiosPlugin.NagiosPlugin):


    def getPage(self, objCommandLine, objUrl):

        from modules import timer


        #http://stackoverflow.com/questions/265720/http-request-timeout
        import socket
        socket.setdefaulttimeout(TIMEOUTSECONDS)
        # will raise a 'socket.timeout' exception upon timeout
        # source : http://bytes.com/topic/python/answers/22953-how-catch-socket-timeout#post84566

        self._objUrl = objUrl
        self._objCommandLine = objCommandLine

        self._getHttpHostHeader()

        myTimer = timer.Timer()
        myTimer.start()
        self._connectToHttpServer()
        self._sendHttpRequest()
        self._getHttpResponse()
        return {
            'httpStatusCode'        : self._httpStatusCode,
            'responseHeaders'       : self._responseHeaders,
            'pageContent'           : self._pageContent,
            'durationMilliseconds'  : myTimer.stop() / 1000
            }


    def _getHttpHostHeader(self):
        if self._objCommandLine.getArgValue('httpHostHeader'):
            self._httpHostHeader = self._objCommandLine.getArgValue('httpHostHeader')
        else:
            self._httpHostHeader = self._objUrl.getHostName()


    def _connectToHttpServer(self):
        # http://docs.python.org/library/httplib.html#httplib.HTTPConnection
        import socket   # required to track the socket.timeout exception
        try:
            self._httpConnection = httplib.HTTPConnection(
                self._objUrl.getHostName(),
                self._objCommandLine.getArgValue('httpPort')
                )
            #TODO : host must be HTTP (no httpS) and have no leading "http://"
        except socket.timeout, e:
            self.exit(
                status      = 'CRITICAL',
                message     = 'Plugin timed out while opening connection.',
                perfdata    = ''
                )


    def _sendHttpRequest(self):
        """
        http://docs.python.org/library/httplib.html#httplib.HTTPConnection.request
        example : http://www.dev-explorer.com/articles/using-python-httplib
        httpConnection.request('GET', '/', {}, {'Host': args.httpHostHeader})
        """
        import socket   # required to track the socket.timeout exception
        try:
            self._httpConnection.request(
                self._objCommandLine.getArgValue('httpMethod'), # method
                self._objUrl.getQuery(),                        # request
                {},                                             # body. Used only for POST (?)
                {'Host': self._httpHostHeader}                  # headers
                )
        except socket.timeout, e:
            self.exit({
                'status'    : 'CRITICAL',
                'message'   : 'Plugin timed out while sending request.',
                'perfdata'  : ''
                })


    def _getHttpResponse(self):
        import socket   # required to track the socket.timeout exception
        try:
            httpResponse = self._httpConnection.getresponse()
            # returns an HTTPResponse object :
            #   http://docs.python.org/library/httplib.html#httplib.HTTPResponse
            #   http://docs.python.org/library/httplib.html#httpresponse-objects

            self._pageContent       = httpResponse.read()
            self._httpStatusCode    = httpResponse.status
            self._responseHeaders   = httpResponse.getheaders()
        except socket.timeout, e:
            self.exit({
                'status'    : 'CRITICAL',
                'message'   : 'Plugin timed out while waiting for response.',
                'perfdata'  : ''
                })


    def _receivedTheExpectedHttpStatusCode(self):
        receivedHttpStatusCode = self._httpStatusCode                       # this is an integer
        expectedHttpStatusCode = int(self._objCommandLine.getArgValue('httpStatusCode'))    # this is passed as a string to the plugin from the command line
        self._objDebug.show('Expected HTTP status code : ' + `expectedHttpStatusCode`)
        self._objDebug.show('Received HTTP status code : ' + `receivedHttpStatusCode`)
        return True if receivedHttpStatusCode == expectedHttpStatusCode else False


    def _matchStringWasFound(self):
#        self._objDebug.show('MatchString : ' + self.getArgValue('matchString'))
#        self._objDebug.show('Received Content : ' + self._pageContent) # <== worth displaying ? this is the full page :-/
        return True if re.search(self._objCommandLine.getArgValue('matchString'), self._pageContent) else False


    def _wasGivenAsPluginParameter(self, params):
#        self._objDebug.show('parameter value : ' + self.getArgValue(params['pluginParameterName']))
#        return True if self.getArgValue(params['pluginParameterName']) != None else False
        return True if self._objCommandLine.getArgValue(params['pluginParameterName']) != None else False


    def checkResult(self):
        """
        The final result is computed in this order :
            1. timeout :                CRITICAL / UNKNOWN if this happens (TODO : make up your mind !). No timeout if we arrive here.
            2. httpStatusCode (default : 200) :         CRITICAL if not received as expected. Otherwise continue
            3. matchString :            CRITICAL if not found. Otherwise continue
            4. warn/crit thresholds :   OK / WARNING / CRITICAL based on values.
        """

#        self._objDebug.show('Expected HTTP status code : ' + self.getArgValue('httpStatusCode'))
        if self._wasGivenAsPluginParameter({'pluginParameterName' : 'httpStatusCode'}) and not self._receivedTheExpectedHttpStatusCode():
            self.exit({
                'status'    : 'CRITICAL',
                'message'   : 'Expected HTTP status code : ' + self._objCommandLine.getArgValue('httpStatusCode') +', received : ' + `self._httpStatusCode`,
                'perfdata'  : '1234'
                })

        if self._wasGivenAsPluginParameter({'pluginParameterName' : 'matchString'}) and not self._matchStringWasFound():
            self.exit({
                'status'    : 'CRITICAL',
                'message'   : 'Expected matchstring "' + self._objCommandLine.getArgValue('matchString') + '" not found',
                'perfdata'  : '1234'
                })



########################################## ##########################################################
# /CLASSES
# CONFIG
########################################## ##########################################################
TIMEOUTSECONDS = 2
########################################## ##########################################################
# /CONFIG
# main()
########################################## ##########################################################


myUtility   = Utility.Utility()
myDebug     = Debug.Debug()

myCommandLine   = CommandLine.CommandLine(
    description = 'Check a web page',
    objDebug    = myDebug, 
    objUtility  = myUtility
    )

myPlugin    = check_web(
    name        = 'CHECK WEB',
    objDebug    = myDebug,
    )

myCommandLine.declareArgument({
    'shortOption'   : 'u',
    'longOption'    : 'url',
    'required'      : True,
    'default'       : None,
    'help'          : 'URL of page to check ()with leading "http://"). To specify a port number, use the "httpPort" directive.',
    'rule'          : 'http://[^:]+'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'p',
    'longOption'    : 'httpPort',
    'required'      : False,
    'default'       : 80,
    'help'          : 'HTTP port (optional. Defaults to 80)',
    'rule'          : '\d+',
    'orArgGroup'    : 'httpMethod_OR_httpPort' # TODO : remove this after testing
    })

myCommandLine.declareArgument({
    'shortOption'   : 'M',
    'longOption'    : 'httpMethod',
    'required'      : False,
    'default'       : 'GET',
    'help'          : 'HTTP method (optional. Defaults to GET)',
    'rule'          : '(GET|POST|HEAD)',
    'orArgGroup'    : 'httpMethod_OR_httpPort' # TODO : remove this after testing
    })

myCommandLine.declareArgument({
    'shortOption'   : 's',
    'longOption'    : 'httpStatusCode',
    'required'      : False,
    'default'       : None,
    'help'          : 'The expected HTTP status code (optional. Defaults to 200)',
    'rule'          : '\d{3}',
    'orArgGroup'    : 'httpStatusCode_OR_matchString'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'm',
    'longOption'    : 'matchString',
    'required'      : False,
    'default'       : None,
    'help'          : 'String to search on page',
    'rule'          : '[\w \.-]+',
    'orArgGroup'    : 'httpStatusCode_OR_matchString'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'w',
    'longOption'    : 'warning',
    'required'      : True,
    'default'       : '',
    'help'          : 'warning threshold in ms',
    'rule'          : '(\d+:?|:\d+|\d+:\d+)'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'c',
    'longOption'    : 'critical',
    'required'      : True,
    'default'       : None,
    'help'          : 'critical threshold in ms',
    'rule'          : ''
    })

myCommandLine.declareArgument({
    'shortOption'   : 'H',
    'longOption'    : 'httpHostHeader',
    'required'      : False,
    'default'       : None,
    'help'          : 'HTTP host header (optional)',
    'rule'          : '[\w\.\-]+'
    })

#"""
#TESTING
myCommandLine.declareArgument({
    'shortOption'   : 'i',
    'longOption'    : 'iii',
    'required'      : False,
    'default'       : None,
    'help'          : '',
    'rule'          : ''
,'orArgGroup':'testing'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'j',
    'longOption'    : 'jjj',
    'required'      : False,
    'default'       : None,
    'help'          : '',
    'rule'          : ''
,'orArgGroup':'testing'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'k',
    'longOption'    : 'kkk',
    'required'      : False,
    'default'       : None,
    'help'          : '',
    'rule'          : ''
,'orArgGroup':'testing'
    })
#/TESTING
#"""

myCommandLine.declareArgumentDebug()
myCommandLine.readArgs()
myCommandLine.showArgs()


myUrl       = Url.Url(full=myCommandLine.getArgValue('url'))


result = myPlugin.getPage(
    objCommandLine  = myCommandLine,
    objUrl          = myUrl
    )

#myDebug.show('HTTP status code : '  + `result['httpStatusCode']`)
#myDebug.show('Duration : '          + `result['durationMilliseconds']` + 'ms')
#myDebug.show('Page length : '       + `len(result['pageContent'])`)
#myDebug.show('Response headers : '  + `result['responseHeaders']`)

myPlugin.checkResult()





# enable myPlugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer














# get result + HTTP exit code

# stop timer
#print myTimer.stop()

# if HTTP exit code is "success", search matchstring
# otherwise, exit with error message + nagios status code

# if matchstring found, report success (nagios status code) + perfdata
# otherwise, report failure + nagios status code + perfdata



########################################## ##########################################################
# /main()
# THE END !
########################################## ##########################################################
