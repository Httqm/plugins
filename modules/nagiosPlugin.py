#!/usr/bin/env python

######################################### nagiosPlugin.py ###########################################
# FUNCTION :	
#
# AUTHOR :	Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :	GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :	1.
#
########################################## ##########################################################


import argparse
import re


class NagiosPlugin(object):

    def __init__(self, params):
        self._name          = params['name']
        self._objDebug      = params['objDebug']
        self._objUtility    = params['objUtility']
        self._exitCodes     = {
            'OK'        : 0,
            'WARNING'   : 1,
            'CRITICAL'  : 2,
            'UNKNOWN'   : 3
            }
#        self._debugIsEnabled = False

#        import argparse
        self._argParser = argparse.ArgumentParser(description = 'Check a web page') # TODO : this is not GENERIC ! Fix it now !
        self._argDict   = {}


    def declareArgument(self, argData):
        """ See : http://docs.python.org/library/argparse.html#the-add-argument-method """
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


    def declareArgumentDebug(self):
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
#            self._objDebug.show('DEBUG IS ENABLED!')


    def _validateArgs(self):
#        self._objDebug.show(self._argDict)
        for argName in self._argDict:
            if argName == 'debug' or not len(self._argDict[argName]['rule']):
                continue
            message = '(for "' + argName + '")' \
                + ' RULE : "' + self._argDict[argName]['rule'] \
                + '", VALUE : "' + str(self._argDict[argName]['value']) + '"'
            if re.search('^' + self._argDict[argName]['rule'] + '$', str(self._argDict[argName]['value'])):
                matchMessage = 'MATCHED :'
            else:
                matchMessage = 'NO MATCH :-('
                self._objDebug.die({'exitMessage': 'Invalid value "' + str(self._argDict[argName]['value']) \
                    + '" for argument "' + argName + '".' \
                    + ' The validation rule (RegExp) is :\n\n\t' + self._argDict[argName]['rule'] + '\n' })
#            self._objDebug.show(matchMessage + ' ' + message)


    def showArgs(self):
        length  = self._objUtility.lengthOfLongestKey(self._argDict)
        for argName in self._argDict:
            print str(argName).rjust(length + 1) + ': ' + str(self._argDict[argName]['value'])
#            print 'RULE : ' + self._argDict[argName]['rule']


    def getArgValue(self, argName):
        return getattr(self._args, argName)


    def _checkArgs(self):
        pass


    def addPerfData(self):
        pass


    def exit(self, params):
        self._mySys = __import__('sys')

        output = self._name + ' : ' + params['status'] + '. ' + params['message'] + '|' + params['perfdata']
        print output
        self._mySys.exit(self._exitCodes[params['status']])


