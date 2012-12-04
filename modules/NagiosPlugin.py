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


okNoWarnString = 'NOWARN (ok)'


class NagiosPlugin(object):

    def __init__(self, name, objDebug):
        self._name          = name
        self._objDebug      = objDebug
        self._exitCodes     = {
            'OK'            : 0,
            okNoWarnString  : 0,
            'WARNING'       : 1,
            'CRITICAL'      : 2,
            'UNKNOWN'       : 3
            }

        self._perfData  = ''
        self._decimalPlaces = 3


    def addPerfData(self, label, value, uom, warn, crit, min=None, max=None):
        """
        Perfdata :  http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201
        Format :    'label'=value[UOM];[warn];[crit];[min];[max]
        """
        self._perfData += label + '=' + str(value) + uom + ';' \
            + str(warn) + ';' + str(crit) + ';' + str(min) + ';' + str(max) + ' '
        self._objDebug.show('PERFDATA : ' + self._perfData)


    def exit(self, exitStatus, exitMessage=''):
        self._mySys = __import__('sys')
        outputMessage = self._name + ' ' + exitStatus + '. ' + exitMessage
        if self._perfData:
            outputMessage += '|' + self._perfData
        print outputMessage
        self._mySys.exit(self._exitCodes[exitStatus])


    def computeExitStatus(self, value, warningThreshold, criticalThreshold):
        """
        Depending on the metric (HDD free / used space), the warn / crit threshold may be inverted :

        Checking used space :

        -oo <--------------+-------------------+---------------------> +oo
                  ok       W      warning      C       critical

        Checking free space :

        -oo <--------------+-------------------+---------------------> +oo
                critical   C      warning      W           ok


        NB : this method doesn't meet the Nagios plugin specification as for warn / crit ranges.
        Since such ranges are not widely used, this implementation should be enough for most common cases.
        """
        # TODO : what about value == warn (or crit) threshold ?

        # TODO : command line parameters may be converted to int earlier ?
        value = int(value)
        warningThreshold    = int(warningThreshold)
        criticalThreshold   = int(criticalThreshold)
        self._objDebug.show('VALUE = ' + str(value) + "\n              WARN  = " \
            + str(warningThreshold) + "\n              CRIT  = " + str(criticalThreshold))



        if warningThreshold == 0 and criticalThreshold == 0:
            exitStatus = okNoWarnString
        else:
            if warningThreshold < criticalThreshold:
                if value < warningThreshold:
                    exitStatus = 'OK'
                elif value > criticalThreshold:
                    exitStatus = 'CRITICAL'
                else:
                    exitStatus = 'WARNING'
            else:
                if value > warningThreshold:
                    exitStatus = 'OK'
                elif value < criticalThreshold:
                    exitStatus = 'CRITICAL'
                else:
                    exitStatus = 'WARNING'




        return exitStatus
