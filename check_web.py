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
#   clear;./check_web.py --url="http://origin-www.voici.fr" --httpHostHeader="www.voici.fr" --httpMethod="GET" --httpStatusCode 301 --matchString="un mot" -w 2500 -c 4000 --debug
#
########################################## ##########################################################

#import urllib  # http://docs.python.org/library/urllib.html?highlight=urllib
import httplib  # http://docs.python.org/library/httplib.htm
import re

from modules import debug
from modules import nagiosPlugin
from modules import url
from modules import utility


########################################## ##########################################################
# CLASSES
########################################## ##########################################################

class check_web(nagiosPlugin.NagiosPlugin):


    def getPage(self, params):

        from modules import timer


        #http://stackoverflow.com/questions/265720/http-request-timeout
        import socket
        socket.setdefaulttimeout(TIMEOUTSECONDS)
        # will raise a 'socket.timeout' exception upon timeout
        # source : http://bytes.com/topic/python/answers/22953-how-catch-socket-timeout#post84566


        self._objUrl = params['objUrl']
#        self._objDebug.show('URL = ' + self.getArgValue('url'))

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


    def _connectToHttpServer(self):
        # http://docs.python.org/library/httplib.html#httplib.HTTPConnection
        import socket   # required to track the socket.timeout exception
        try:
            self._httpConnection = httplib.HTTPConnection(
                self._objUrl.getHostName(),
                self.getArgValue('httpPort'),
#                timeout = TIMEOUTSECONDS   # this is managed globally
                )
            #TODO : host must be HTTP (no httpS) and have no leading "http://"
        except socket.timeout, e:
            self._objDebug.die({'exitMessage': "Error during connection: %s" % e}) # TODO : replace this by a 'Nagios exit', as critical


    def _sendHttpRequest(self):
        """
        http://docs.python.org/library/httplib.html#httplib.HTTPConnection.request
        example : http://www.dev-explorer.com/articles/using-python-httplib
        httpConnection.request('GET', '/', {}, {'Host': args.httpHostHeader})
        """
        import socket   # required to track the socket.timeout exception
        self._objDebug.show('URL query = ' + self._objUrl.getQuery())
        try:
            self._httpConnection.request(
                self.getArgValue('httpMethod'),                 # method
                self._objUrl.getQuery(),                        # request
                {},                                             # body. Used only for POST (?)
                {'Host': self.getArgValue('httpHostHeader')}    # headers
                )
        except socket.timeout, e:
            self._objDebug.die({'exitMessage': "Error while sending request: %s" % e}) # TODO : replace this by a 'Nagios exit', as critical


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
            self._objDebug.die({'exitMessage': "Error while getting response: %s" % e}) # TODO : replace this by a 'Nagios exit', as critical


    def _receivedTheExpectedHttpStatusCode(self):
        receivedHttpStatusCode = self._httpStatusCode                       # this is an integer
        expectedHttpStatusCode = int(self.getArgValue('httpStatusCode'))    # this is passed as a string to the plugin from the command line
        self._objDebug.show('Expected HTTP status code : ' + `expectedHttpStatusCode`)
        self._objDebug.show('Received HTTP status code : ' + `receivedHttpStatusCode`)
        return True if receivedHttpStatusCode == expectedHttpStatusCode else False


    def _matchStringWasFound(self):
        self._objDebug.show('MatchString : ' + `self.getArgValue('matchString')`)
        self._objDebug.show('Received Content : ' + `self._pageContent`)
        return True if re.search(self.getArgValue('matchString'), self._pageContent) else False


    def checkResult(self):
        if not self._receivedTheExpectedHttpStatusCode():
#            self._objDebug.die({'exitMessage': "Did not receive the expected HTTP status code"}) # TODO with a 'Nagios exit', as critical
            self.exit({
                'status'    : 'CRITICAL',
                'message'   : 'Expected HTTP status code : ' + self.getArgValue('httpStatusCode') +', received : ' + `self._httpStatusCode`,
                'perfdata'  : '1234'
                })


########################################## ##########################################################
# /CLASSES
# CONFIG
########################################## ##########################################################
TIMEOUTSECONDS = 5
########################################## ##########################################################
# /CONFIG
# main()
########################################## ##########################################################


myUtility   = utility.Utility()
myDebug     = debug.Debug()


myPlugin    = check_web({
    'name'          : 'CHECK WEB',
    'objDebug'      : myDebug,
    'objUtility'    : myUtility
    })

myPlugin.declareArgument({
    'shortOption'   : 'u',
    'longOption'    : 'url',
    'required'      : True,
    'default'       : None,
    'help'          : 'URL of page to check ()with leading "http://"). To specify a port number, use the "httpPort" directive.',
    'rule'          : 'http://[^:]*'
    })

myPlugin.declareArgument({
    'shortOption'   : 'p',
    'longOption'    : 'httpPort',
    'required'      : False,
    'default'       : 80,
    'help'          : 'HTTP port (optional. Defaults to 80)',
    'rule'          : '\d+'
    })

myPlugin.declareArgument({
    'shortOption'   : 'M',
    'longOption'    : 'httpMethod',
    'required'      : False,
    'default'       : 'GET',
    'help'          : 'HTTP method (optional. Defaults to GET)',
    'rule'          : '(GET|POST|HEAD)'
    })

myPlugin.declareArgument({
    'shortOption'   : 's',
    'longOption'    : 'httpStatusCode',
    'required'      : False,
    'default'       : '200',
    'help'          : 'The expected HTTP status code (optional. Defaults to 200)',
    'rule'          : '\d{3}'
    })

myPlugin.declareArgument({
    'shortOption'   : 'm',
    'longOption'    : 'matchString',
    'required'      : True,
    'default'       : None,
    'help'          : 'String to search on page',
    'rule'          : '[\w ]+'
    })

myPlugin.declareArgument({
    'shortOption'   : 'w',
    'longOption'    : 'warning',
    'required'      : True,
    'default'       : None,
    'help'          : 'warning threshold in ms',
    'rule'          : '(\d+:?|:\d+|\d+:\d+)'
    })

myPlugin.declareArgument({
    'shortOption'   : 'c',
    'longOption'    : 'critical',
    'required'      : True,
    'default'       : None,
    'help'          : 'critical threshold in ms',
    'rule'          : ''
    })

myPlugin.declareArgument({
    'shortOption'   : 'H',
    'longOption'    : 'httpHostHeader',
    'required'      : True,
    'default'       : None,
    'help'          : 'HTTP host header (optional)',
    'rule'          : '[\w\.\-]*'
    })

myPlugin.declareArgumentDebug()
myPlugin.readArgs()
myPlugin.showArgs()

#myDebug.show('url = ' + myPlugin.getArgValue('url'))

myUrl       = url.Url({
    'full'  : myPlugin.getArgValue('url')
    })


result = myPlugin.getPage({'objUrl' : myUrl})

myDebug.show('HTTP status code : '  + `result['httpStatusCode']`)
myDebug.show('Duration : '          + `result['durationMilliseconds']` + 'ms')
myDebug.show('Page length : '       + `len(result['pageContent'])`)
myDebug.show('Response headers : '  + `result['responseHeaders']`)

myPlugin.checkResult()

# We're happy if :
# - the HTTP status code we received is the expected one
# - AND the match string is found in the returned content
# - AND all of this happens BEFORE the timeout



#myDebug.die({'exitMessage': 'ARGL !'})


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
