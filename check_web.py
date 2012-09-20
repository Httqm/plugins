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
import re

from modules import debug
from modules import nagiosPlugin
from modules import url
from modules import timer
from modules import utility


########################################## ##########################################################
# CLASSES
########################################## ##########################################################

class check_web(nagiosPlugin.NagiosPlugin):

    def getPage(self, params):

        self._objUrl = params['objUrl']
#        self._objDebug.show('URL = ' + self.getArgValue('url'))

        self._connectToHttpServer()
        self._sendHttpRequest()
        self._getHttpResponse()
        self._leaveIfNonOkHttpStatusCode()


    def _connectToHttpServer(self):
        # http://docs.python.org/library/httplib.html#httplib.HTTPConnection
        self._httpConnection = httplib.HTTPConnection(
            self._objUrl.getHostName(),
            self.getArgValue('httpPort'),
            timeout = 10
            )
        #TODO : host must be HTTP (no httpS) and have no leading "http://"


    def _sendHttpRequest(self):
        """
        example : http://www.dev-explorer.com/articles/using-python-httplib
        httpConnection.request('GET', '/', {}, {'Host': args.httpHostHeader})
        """
        self._httpConnection.request(
            self.getArgValue('httpMethod'),
            '/', # TODO : this is the HTTP request
            {},
            {'Host': self.getArgValue('httpHostHeader')}
            )


    def _getHttpResponse(self):
        httpResponse = self._httpConnection.getresponse()
        # returns an HTTPResponse object :
        #   http://docs.python.org/library/httplib.html#httplib.HTTPResponse
        #   http://docs.python.org/library/httplib.html#httpresponse-objects

        self._objDebug.show(httpResponse.read())
        self._httpStatusCode = httpResponse.status
        self._objDebug.show(self._httpStatusCode)


    def _leaveIfNonOkHttpStatusCode(self):
        self._objDebug.show(HTTPOKSTATUSES)
        if not self._httpStatusCode in HTTPOKSTATUSES:
            self._objDebug.die({'exitMessage': 'HTTP failed !'})
            # TODO : implement the "plugin exit", with nagios status code stuff


########################################## ##########################################################
# /CLASSES
# CONFIG
########################################## ##########################################################
HTTPOKSTATUSES = [ 200, 301, 302 ]

########################################## ##########################################################
# /CONFIG
# main()
########################################## ##########################################################

myTimer     = timer.Timer()
myTimer.start()

import time
time.sleep(1) # 1 second, but displayed time, in us is ~1000 WTF ? Should be ~1 000 000
print myTimer.stop()



myUtility   = utility.Utility()
myDebug     = debug.Debug()

myDebug.die({'exitMessage':'argl2'})

myPlugin    = check_web({
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

myPlugin.getPage({'objUrl' : myUrl})



#myDebug.die({'exitMessage': 'ARGL !'})


# enable myPlugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer














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
