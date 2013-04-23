#!/usr/bin/env python3
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


    def test1_computeExitStatus(self):
        """
        Given a CPU load < warn threshold
	should return the 'OK' Nagios plugin exit status
        """
        self._objUtility    = Utility.Utility()
        self._objDebug      = Debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            objDebug    = self._objDebug,
            )

        myPlugin.cpuUsagePercent = warning - 1

        exitStatus = myPlugin.computeExitStatus(warningThreshold=warning, criticalThreshold=critical)
        self.assertEqual(exitStatus, 'OK')


    def test2_computeExitStatus(self):
        """
        Given a warn threshold < CPU load < crit threshold
	should return the 'WARNING' Nagios plugin exit status
        """
        self._objUtility    = Utility.Utility()
        self._objDebug      = Debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            objDebug    = self._objDebug,
            )

        myPlugin.cpuUsagePercent = critical - 1

        exitStatus = myPlugin.computeExitStatus(warningThreshold=warning, criticalThreshold=critical)
        self.assertEqual(exitStatus, 'WARNING')


    def test3_computeExitStatus(self):
        """
        Given a CPU load > crit threshold
	should return the 'CRITICAL' Nagios plugin exit status
        """
        self._objUtility    = Utility.Utility()
        self._objDebug      = Debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            objDebug    = self._objDebug,
            )

        myPlugin.cpuUsagePercent = critical + 1

        exitStatus = myPlugin.computeExitStatus(warningThreshold=warning, criticalThreshold=critical)
        self.assertEqual(exitStatus, 'CRITICAL')


# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
