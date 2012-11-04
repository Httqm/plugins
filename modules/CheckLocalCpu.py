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
# MODULE PART
#
# VERSION :     20121024
########################################## ##########################################################

import NagiosPlugin
import psutil


class CheckLocalCpu(NagiosPlugin.NagiosPlugin):

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
        debugTotalPercents  = 0
        debugCpuUsages      = ''

        self._cpuData['totalWithoutIdle'] = {'cpuPercent': 0}
        for fieldName in self._fields:
            self._cpuData[fieldName]['cpuPercent'] = self._objUtility.computePercentage(self._cpuData[fieldName]['cpuTime'], self._totalTime)
            debugCpuUsages += fieldName + ' : ' + `self._cpuData[fieldName]['cpuPercent']` + ' %' + '\n'
            debugTotalPercents += self._cpuData[fieldName]['cpuPercent']
            if fieldName != 'idle':
                self._cpuData['totalWithoutIdle']['cpuPercent'] += self._cpuData[fieldName]['cpuPercent'] 

        # DEBUG
#        self._objDebug.show(self._cpuData)
#        self._objDebug.show('CPU USAGES : ' + debugCpuUsages)
#        self._objDebug.show('total percents               = ' + `debugTotalPercents` + '%' \
#            "\n              total percents (except idle) = " + `self._cpuData['totalWithoutIdle']['cpuPercent']` + '%')
        # /DEBUG
        self._cpuUsagePercent = self._cpuData['totalWithoutIdle']['cpuPercent']

        
    def computeOutput(self, warningThreshold, criticalThreshold):
        """
        Compare the 'totalWithoutIdle' CPU time VS the warn / crit thresholds
        and return the corresponding exit code.
        """
        cpuUsage = self._cpuData['totalWithoutIdle']['cpuPercent']
        self._objDebug.show('CPU usage : ' + `cpuUsage` + '%' \
            + "\nWarning threshold : " + `warningThreshold` \
            + "\nCritical threshold : " + `criticalThreshold` )

        self._exitCode = None
        if(cpuUsage < warningThreshold):
            self._exitCode = self._exitCodes['OK']
        elif(cpuUsage > criticalThreshold):
            self._exitCode = self._exitCodes['CRITICAL']
        else:
            self._exitCode = self._exitCodes['WARNING']
        self._objDebug.show('Exit code : ' + `self._exitCode`)


#    def buildPerfData(self):
#        self.addPerfData(
#            label   = 'CPU usage',
#            value   = self._cpuUsagePercent,
#            uom     = '%',
#            warn    = self.getArgValue('warning'),
#            crit    = self.getArgValue('critical'),
#            min     = 0,
#            max     =100)
#	#self._perfData = 'CPU usage : ' + self._cpuData['totalWithoutIdle']['cpuPercent'] + '%'

