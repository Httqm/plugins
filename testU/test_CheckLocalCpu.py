#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


########################################## ##########################################################
# allows importing from parent folder
# source : http://stackoverflow.com/questions/714063/python-importing-modules-from-parent-folder
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
########################################## ##########################################################


from modules import CheckLocalCpu
from modules import Utility
from modules import Debug


warning     = 75
critical    = 90


class test_CheckLocalCpu(unittest.TestCase):


    def test1_computeExitCode(self):
        """
        Given a CPU load < warn threshold
	should return the 'OK' Nagios plugin exit code
        """
        self._objUtility    = Utility.Utility()
        self._objDebug      = Debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            description = 'Check the local CPU usage.',
            objDebug    = self._objDebug,
            objUtility  = self._objUtility
            )

        myPlugin._cpuData = {
#            'softirq'   : {'cpuPercent': 1.0,   'cpuTime': 12.12},
#            'iowait'    : {'cpuPercent': 1.0,   'cpuTime': 12.12},
#            'system'    : {'cpuPercent': 1.0,   'cpuTime': 12.12},
#            'idle'      : {'cpuPercent': 90.0,  'cpuTime': 12.12},
#            'user'      : {'cpuPercent': 5.0,   'cpuTime': 12.12},
#            'irq'       : {'cpuPercent': 1.0,   'cpuTime': 12.12},
#            'nice'      : {'cpuPercent': 1.0,   'cpuTime': 12.12},

#            'totalWithoutIdle'      : {'cpuPercent': 76.0,   'cpuTime': 12.12}
            'totalWithoutIdle': {'cpuPercent': warning - 1, 'cpuTime': 12.34}
            }

        myPlugin.computeExitCode(warningThreshold=warning, criticalThreshold=critical)
        self.assertEqual(myPlugin._exitCode, myPlugin._exitCodes['OK'])


    def test2_computeExitCode(self):
        """
        Given a warn threshold < CPU load < crit threshold
	should return the 'WARNING' Nagios plugin exit code
        """
        self._objUtility    = Utility.Utility()
        self._objDebug      = Debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            description = 'Check the local CPU usage.',
            objDebug    = self._objDebug,
            objUtility  = self._objUtility
            )

        myPlugin._cpuData = {
            'totalWithoutIdle': {'cpuPercent': critical - 1, 'cpuTime': 12.34}
            }

        myPlugin.computeExitCode(warningThreshold=warning, criticalThreshold=critical)
        self.assertEqual(myPlugin._exitCode, myPlugin._exitCodes['WARNING'])


    def test3_computeExitCode(self):
        """
        Given a CPU load > crit threshold
	should return the 'CRITICAL' Nagios plugin exit code
        """
        self._objUtility    = Utility.Utility()
        self._objDebug      = Debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            description = 'Check the local CPU usage.',
            objDebug    = self._objDebug,
            objUtility  = self._objUtility
            )

        myPlugin._cpuData = {
            'totalWithoutIdle': {'cpuPercent': critical + 1, 'cpuTime': 12.34}
            }

        myPlugin.computeExitCode(warningThreshold=warning, criticalThreshold=critical)
        self.assertEqual(myPlugin._exitCode, myPlugin._exitCodes['CRITICAL'])

        

# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
