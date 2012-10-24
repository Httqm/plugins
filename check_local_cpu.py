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

######################################### check_local_cpu.py ##############################################
# FUNCTION :    This plugin 
#
# VERSION :     20121023
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


import psutil
from modules import debug
from modules import nagiosPlugin
from modules import utility


########################################## ##########################################################
# CLASSES
########################################## ##########################################################

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

class check_local_cpu(nagiosPlugin.NagiosPlugin):

    def getCpuTimes(self):
        # help with named tuples :
        # http://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python
        # http://pysnippet.blogspot.fr/2010/01/named-tuple.html
        self._cpuTimes  = psutil.cpu_times()
        self._cpuData   = {}
#        print self._cpuTimes.user
        self._fields    = ['user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq']
        self._totalTime = 0
        for fieldName in self._fields:
#            print fieldName
            self._cpuData[fieldName] = {}
            time = getattr(self._cpuTimes, fieldName)
            self._cpuData[fieldName]['cpuTime'] = time
            self._totalTime += time
#        print self._cpuData

    def computeCpuUsagePercent(self):
#        total = 0
        for fieldName in self._fields:
            self._cpuData[fieldName]['cpuPercent'] = myUtility.computePercentage(self._cpuData[fieldName]['cpuTime'], self._totalTime)
            self._objDebug.show(fieldName + ' : ' + `self._cpuData[fieldName]['cpuPercent']` + ' %')
#            total += self._cpuData[fieldName]['cpuPercent']
#        print 'total percents = ' + `total` + '%'

        

########################################## ##########################################################
# /CLASSES
# CONFIG
########################################## ##########################################################

########################################## ##########################################################
# /CONFIG
# main()
########################################## ##########################################################

myUtility   = utility.Utility()

#print "PERCENTAGE"
#print myUtility.computePercentage(10, 100)

myDebug     = debug.Debug()

myPlugin    = check_local_cpu(
    name        = 'CHECK LOCAL CPU',
    objDebug    = myDebug,
    objUtility  = myUtility
    )

myPlugin.declareArgument({
    'shortOption'   : 'w',
    'longOption'    : 'warning',
    'required'      : True,
    'default'       : '',
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


myPlugin.declareArgumentDebug()
myPlugin.readArgs()
myPlugin.showArgs()


myPlugin.getCpuTimes()
myPlugin.computeCpuUsagePercent()
"""

myPlugin.declareArgumentDebug()
myPlugin.readArgs()
myPlugin.showArgs()


myUrl       = url.Url(full=myPlugin.getArgValue('url'))


result = myPlugin.getPage(objUrl=myUrl)

#myDebug.show('HTTP status code : '  + `result['httpStatusCode']`)
#myDebug.show('Duration : '          + `result['durationMilliseconds']` + 'ms')
#myDebug.show('Page length : '       + `len(result['pageContent'])`)
#myDebug.show('Response headers : '  + `result['responseHeaders']`)

myPlugin.checkResult()


# enable myPlugin timeout + interrupt. If timeout, exit as nagios status code "unknown" + exit message

# init timer

"""

########################################## ##########################################################
# /main()
# THE END !
########################################## ##########################################################
