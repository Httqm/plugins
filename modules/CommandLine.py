#!/usr/bin/env python

######################################### CommandLine.py ############################################
# FUNCTION :
#
# AUTHOR :	Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :	GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :	1.
#
########################################## ##########################################################

# TODO : define rules such as w < c, or w > c, and check them



import argparse
import re


class CommandLine(object):

########################################## ##########################################################
# CONSTRUCTOR

    def __init__(self, description, objDebug, objUtility):
        self._objDebug      = objDebug
        self._objUtility    = objUtility

        self._argParser = argparse.ArgumentParser(description = description)
        # The "description" field will be displayed when invoking help (-h)

        self._argDict   = {}
        self._perfData  = ''
        self._decimalPlaces = 3


########################################## ##########################################################
#

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
#        self._checkOrArgGroups()    # TODO : not the right place to do this. FIX IT!


    def showArgs(self):
        length  = self._objUtility.lengthOfLongestKey(self._argDict)
        message = ''
        for argName in self._argDict:
            message += '\n' + str(argName).rjust(length + 1) + ': ' + str(self._argDict[argName]['value'])
        self._objDebug.show(message)


    def getArgValue(self, argName):
        return getattr(self._args, argName)


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

    def checkArgsMatchRules(self):
        allArgsMatchRules = True
#        self._objDebug.show(self._argDict)
        for argName in self._argDict:
            if self._isUselessCheckingArgument(argName):
                continue
            if re.search('^' + self._argDict[argName]['rule'] + '$', str(self._argDict[argName]['value'])):
                matchMessage = 'MATCHED :'
                thisArgIsOk = True
            else:
                matchMessage = 'NO MATCH :-('
#                self._objDebug.die(exitMessage = 'Invalid value "' + str(self._argDict[argName]['value']) \
#                    + '" for argument "' + argName + '".' \
#                    + ' The validation rule (RegExp) is :\n\n\t' + self._argDict[argName]['rule'] + '\n')
                thisArgIsOk = False
#            message = '(for "' + argName + '")' \
#                + ' RULE : "' + self._argDict[argName]['rule'] \
#                + '", VALUE : "' + str(self._argDict[argName]['value']) + '"'
#            self._objDebug.show(matchMessage + ' ' + message)
            allArgsMatchRules = allArgsMatchRules and thisArgIsOk

        return allArgsMatchRules


    def _isUselessCheckingArgument(self, argName):
        if argName == 'debug' \
            or len(self._argDict[argName]['rule']) == 0 \
            or self._argDict[argName]['value'] == None:
            return True
        else:
            return False


########################################## ##########################################################
# THE 'ORARGGROUPS'

    def _getOrArgGroup(self, argData):  # TODO : stop using dicts as arguments !!!
        """
        'Or arg. groups' are groups of optional arguments where AT LEAST 1 argument MUST BE provided.
        """
        try:
            return argData['orArgGroup']
        except KeyError:
            return None


    def checkOrArgGroups(self):
        self._getOrArgGroupsData()
        return self._detectOrArgGroupsMissingArgs()


    def _getOrArgGroupsData(self):
#        self._objDebug.show(self._argDict)
        groups = {}

        # TODO : many nested blocks. check this !
        for argName in self._argDict:
            groupName = self._argDict[argName]['orArgGroup']    # because readability matters !
            if groupName:
                argWasProvided = False if self._argDict[argName]['value'] == None else True
                if groupName in groups:
                    groups[groupName]['status'] = groups[groupName]['status'] or argWasProvided
                else:
                    groups[groupName] = {'status': argWasProvided, 'arguments': [] }

                groups[groupName]['arguments'].append(argName)
        self._orArgGroupsData = groups


    def _detectOrArgGroupsMissingArgs(self):
#        self._objDebug.show(self._orArgGroupsData)
        orArgGroupsAreOkay  = True
        message             = ''
        for groupName in self._orArgGroupsData:
#            self._objDebug.show(groupName + ' ' + str(self._orArgGroupsData[groupName]['status']) + ' ' + str(self._orArgGroupsData[groupName]['arguments']))
            orArgGroupsAreOkay = orArgGroupsAreOkay and self._orArgGroupsData[groupName]['status']
            if not self._orArgGroupsData[groupName]['status']:
                message += 'One of these command-line arguments is missing : ' \
                    + str(self._orArgGroupsData[groupName]['arguments']) + '\n'
#        self._objDebug.show(str(orArgGroupsAreOkay) + ', "' + message + '"')
        return orArgGroupsAreOkay, message
