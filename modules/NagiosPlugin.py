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

########################################## ##########################################################
# CONSTRUCTOR

    def __init__(self, name, objDebug, objUtility):
        self._name          = name
        self._objDebug      = objDebug
        self._objUtility    = objUtility
        self._exitCodes     = {
            'OK'        : 0,
            'WARNING'   : 1,
            'CRITICAL'  : 2,
            'UNKNOWN'   : 3
            }
        self._argParser = argparse.ArgumentParser(description = 'Check a web page') # TODO : this is not GENERIC ! Fix it now !
        self._argDict   = {}


########################################## ##########################################################
# PUBLIC METHODS

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
            'value'         : 0,
            'rule'          : argData['rule'],
            'orArgGroup'    : self._getOrArgGroup(argData)
            }


    def readArgs(self):
        self._args = self._argParser.parse_args()
        for argName in self._argDict:
            self._argDict[argName]['value'] = getattr(self._args, argName)
        self._detectDebugValue()
        self._checkOrArgGroups()
        self._validateArgs()


    def showArgs(self):
        length  = self._objUtility.lengthOfLongestKey(self._argDict)
        for argName in self._argDict:
            print str(argName).rjust(length + 1) + ': ' + str(self._argDict[argName]['value'])
#            print 'RULE : ' + self._argDict[argName]['rule']


    def getArgValue(self, argName):
        return getattr(self._args, argName)


    def exit(self, status, message, perdata):
        self._mySys = __import__('sys')

        output = self._name + ' : ' + status + '. ' + message + '|' + perfdata
        print output
        self._mySys.exit(self._exitCodes[status])


########################################## ##########################################################
# THE 'DEBUG' COMMAND LINE ARGUMENT

    def declareArgumentDebug(self):
        self._argParser.add_argument(
            '--debug',
            required    = False,
            action      = 'store_true',
            help        = 'Toggle debug messages'
            )
        self._argDict['debug'] = {'orArgGroup': None}


    def _detectDebugValue(self):
        if self._argDict['debug']['value']:
            self._objDebug.enable(True)
#            self._objDebug.show('DEBUG IS ENABLED!')


########################################## ##########################################################
# ARGUMENTS VALIDATION

    def _validateArgs(self):
#        self._objDebug.show(self._argDict)
        for argName in self._argDict:
            if self._isUselessCheckingArgument(argName):
                continue
            if re.search('^' + self._argDict[argName]['rule'] + '$', str(self._argDict[argName]['value'])):
                matchMessage = 'MATCHED :'
            else:
                matchMessage = 'NO MATCH :-('
                self._objDebug.die(exitMessage = 'Invalid value "' + str(self._argDict[argName]['value']) \
                    + '" for argument "' + argName + '".' \
                    + ' The validation rule (RegExp) is :\n\n\t' + self._argDict[argName]['rule'] + '\n')
#            message = '(for "' + argName + '")' \
#                + ' RULE : "' + self._argDict[argName]['rule'] \
#                + '", VALUE : "' + str(self._argDict[argName]['value']) + '"'
#            self._objDebug.show(matchMessage + ' ' + message)


    def _isUselessCheckingArgument(self, argName):
        if argName == 'debug' \
            or len(self._argDict[argName]['rule']) == 0 \
            or self._argDict[argName]['value'] == None:
            return True
        else:
            return False


########################################## ##########################################################
# THE 'ORARGGROUPS'

    def _getOrArgGroup(self, argData):
        """
        'Or arg. groups' are groups of optional arguments where AT LEAST 1 argument MUST BE provided.
        """
        try:
            return argData['orArgGroup']
        except KeyError:
            return None


    def _checkOrArgGroups(self):
        self._getOrArgGroupsData()
        self._alertOrArgGroupsMissingArgs()


    def _getOrArgGroupsData(self):
        self._objDebug.show(self._argDict)
        groups = {}
        for argName in self._argDict:
            groupName = self._argDict[argName]['orArgGroup']    # because readability matters !
#            print argName + ' ' + str(groupName) + ' ' + str(self._argDict[argName]['value'])
            if groupName:
                argWasProvided = False if self._argDict[argName]['value'] == None else True
                if groupName in groups:
                    groups[groupName]['status'] = groups[groupName]['status'] or argWasProvided
                else:
                    groups[groupName] = {'status': argWasProvided, 'arguments': [] }

                groups[groupName]['arguments'].append(argName)
        self._orArgGroupsData = groups


    def _alertOrArgGroupsMissingArgs(self):
        self._objDebug.show(self._orArgGroupsData)
        orArgGroupsAreOkay  = True
        message             = ''
        for groupName in self._orArgGroupsData:
            print groupName + ' ' + str(self._orArgGroupsData[groupName]['status']) + ' ' + str(self._orArgGroupsData[groupName]['arguments'])
            orArgGroupsAreOkay = orArgGroupsAreOkay and self._orArgGroupsData[groupName]['status']
            if not self._orArgGroupsData[groupName]['status']:
                message += 'One of these arguments is missing : ' + str(self._orArgGroupsData[groupName]['arguments']) + '\n'
        print message
        # TODO : do a 'nagios exit'

########################################## ##########################################################

    def _checkArgs(self):
        pass


    def addPerfData(self):
        pass
