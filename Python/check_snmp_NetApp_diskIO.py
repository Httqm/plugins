#!/usr/bin/env python3

# check_snmp_NetApp_diskIO.py - Copyright (C) 2013 Matthieu FOURNET, fournet.matthieu@gmail.com
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

######################################### check_snmp_NetApp_diskIO.py ###############################
# FUNCTION :    This plugin ...
#
# VERSION :     20130311
#
# COMMAND LINE :    (the scissors 8< mean the command continues on the next line)
#       ./check_snmp_NetApp_diskIO.py -w xxx -c yyy --debug
#
# NOTES :	1. Required 'pysnmp' (http://pysnmp.sourceforge.net/)
#                   installed with 'pip install pysnmp'
#
# KNOWN BUGS AND LIMITATIONS :
#               1.
#
########################################## ##########################################################

"""

"""

from modules import CommandLine
from modules import Check_snmp_NetApp_diskIO
from modules import Debug
from modules import Utility

myUtility   = Utility.Utility()
myDebug     = Debug.Debug()

myCommandLine = CommandLine.CommandLine(
    description = 'Check NetApp disks I/O through SNMP.',
    objDebug    = myDebug,
    objUtility  = myUtility
    )

myPlugin    = CheckLocalCpu.CheckLocalCpu(
    name        = 'CHECK NETAPP DISK IO',
    objDebug    = myDebug,
    )

myCommandLine.declareArgument({
    'shortOption'   : 'w',
    'longOption'    : 'warning',
    'required'      : True,
    'default'       : '',
    'help'          : 'warning threshold in %%',    # '%%' escapes the '%' sign
    'rule'          : '(\d+:?|:\d+|\d+:\d+)'
    })

myCommandLine.declareArgument({
    'shortOption'   : 'c',
    'longOption'    : 'critical',
    'required'      : True,
    'default'       : None,
    'help'          : 'critical threshold in %%',
    'rule'          : '(\d+:?|:\d+|\d+:\d+)'
    })

myCommandLine.declareArgumentDebug()
myCommandLine.readArgs()
#myCommandLine.showArgs()

if not myCommandLine.checkArgsMatchRules():
    myPlugin.exit(
        exitStatus  = 'UNKNOWN',
        exitMessage = 'args dont match rules :-(')

# TODO : check that warning < critical and that kind of things ;-)


myPlugin.getCpuUsagePercent()


#myDebug.show('WARNING = ' + myPlugin.getArgValue('warning'))
#myDebug.show('CRITICAL = ' + myPlugin.getArgValue('critical'))

exitStatus = myPlugin.computeExitStatus(
    warningThreshold    = myCommandLine.getArgValue('warning'),
    criticalThreshold   = myCommandLine.getArgValue('critical')
    )


myPlugin.addPerfData(
    label   = 'NetApp disk IO',
    value   = myPlugin.cpuUsagePercent,
    uom     = '%',
    warn    = myCommandLine.getArgValue('warning'),
    crit    = myCommandLine.getArgValue('critical'),
    min     = 0,
    max     =100)

# TODO : determine exitStatus
myPlugin.exit(exitStatus  = exitStatus)


