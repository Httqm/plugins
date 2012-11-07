#!/usr/bin/env python

# check_local_cpu.py - Copyright (C) 2012 Matthieu FOURNET, fournet.matthieu@gmail.com
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

######################################### check_local_cpu.py ########################################
# FUNCTION :    This plugin ...
#
# VERSION :     20121024
#
# COMMAND LINE :    (the scissors 8< mean the command continues on the next line)
#       ./check_local_cpu.py -w 75 -c 90 --debug
#
# NOTES :	1. This plugin requires the "psutil" library (http://code.google.com/p/psutil/).
#                   Install it with :
#                      pip install psutil
#                   Installing "psutil" this way requires the (Debian) packages :
#                       python-pip
#                       python-dev
#
# KNOWN BUGS AND LIMITATIONS :
#               1. 
#
########################################## ##########################################################


from modules import CommandLine
from modules import CheckLocalCpu
from modules import Debug
from modules import Utility

myUtility   = Utility.Utility()
myDebug     = Debug.Debug()

myCommandLine = CommandLine.CommandLine(
    description = 'Check the local CPU usage.',
    objDebug    = myDebug,
    objUtility  = myUtility
    )

myPlugin    = CheckLocalCpu.CheckLocalCpu(
    name        = 'CHECK LOCAL CPU',
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


myPlugin.getCpuUsagePercent()




#myDebug.show('WARNING = ' + myPlugin.getArgValue('warning'))
#myDebug.show('CRITICAL = ' + myPlugin.getArgValue('critical'))

myPlugin.computeExitCode(
    warningThreshold    = myCommandLine.getArgValue('warning'),
    criticalThreshold   = myCommandLine.getArgValue('critical')
    )


myPlugin.addPerfData(
    label   = 'CPU usage',
    value   = myPlugin.cpuUsagePercent,
    uom     = '%',
    warn    = myCommandLine.getArgValue('warning'),
    crit    = myCommandLine.getArgValue('critical'),
    min     = 0,
    max     =100)

# TODO : determine exitStatus
myPlugin.exit(exitStatus  = 'UNKNOWN')



"""
PLAYING WITH psutil :

for x in range(3):
    print psutil.cpu_percent(interval=1)

print
print psutil.cpu_percent(interval=0.1)
print psutil.cpu_percent(interval=1)


cpuTimes = psutil.cpu_times()

print cpuTimes
# user, nice, system, idle, iowait, irq, softirq

for truc in cpuTimes:
    print truc
"""
