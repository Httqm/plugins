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

import nagiosPlugin
import psutil


class CheckLocalCpu(nagiosPlugin.NagiosPlugin):

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
            self._cpuData[fieldName]['cpuPercent'] = self._objUtility.computePercentage(self._cpuData[fieldName]['cpuTime'], self._totalTime)
            self._objDebug.show(fieldName + ' : ' + `self._cpuData[fieldName]['cpuPercent']` + ' %')
#            total += self._cpuData[fieldName]['cpuPercent']
#        print 'total percents = ' + `total` + '%'

        
    def computeOutput(self):
        """
        Check the highest of CPU usages, and check it against the warn/crit thresholds
        """
        pass


    def buildPerfData(self):
        pass


    def exit(self):
        pass
