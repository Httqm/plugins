#!/usr/bin/env python

######################################### NagiosPlugin.py ###########################################
# FUNCTION :
#
# AUTHOR :	Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :	GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :	1.
#
########################################## ##########################################################


class NagiosPlugin(object):

#    def __init__(self, name, objDebug, objUtility):
    def __init__(self, name, objDebug):
        self._name          = name
        self._objDebug      = objDebug
#        self._objUtility    = objUtility
        self._exitCodes     = {
            'OK'        : 0,
            'WARNING'   : 1,
            'CRITICAL'  : 2,
            'UNKNOWN'   : 3
            }

        self._perfData  = ''
        self._decimalPlaces = 3


    def addPerfData(self, label, value, uom, warn, crit, min, max):
        """
        Perfdata :  http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201
        Format :    'label'=value[UOM];[warn];[crit];[min];[max]
        """
        self._perfData += label + '=' + str(value) + uom + ';' \
            + str(warn) + ';' + str(crit) + ';' + str(min) + ';' + str(max) + ' '
        self._objDebug.show('PERFDATA : ' + self._perfData)


#    def exit(self):
#        self._mySys = __import__('sys')
#        print self._name + ' ' + self._exitStatus + '|' + self._perfData
#        self._mySys.exit(self._exitCode)


    def exit(self, exitStatus, exitMessage=''):
        self._mySys = __import__('sys')
        outputMessage = self._name + ' ' + exitStatus + '. ' + exitMessage
        if self._perfData:
            outputMessage += '|' + self._perfData
        print outputMessage
        self._mySys.exit(self._exitCodes[exitStatus])
