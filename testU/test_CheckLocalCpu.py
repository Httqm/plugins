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
from modules import utility
from modules import debug


class test_CheckLocalCpu(unittest.TestCase):

    def test1_computeOutput(self):
        """
        Given a CPU load < warn threshold
	should return any of the 'OK' Nagios plugin exit code
        """
        self._objUtility    = utility.Utility()
        self._objDebug      = debug.Debug()
        myPlugin    = CheckLocalCpu.CheckLocalCpu(
            name        = 'CHECK LOCAL CPU',
            objDebug    = self._objDebug,
            objUtility  = self._objUtility
            )

#        self._cpuData = {'softirq': {'cpuPercent': 0.003871639406714247, 'cpuTime': 260.79000000000002}, 'iowait': {'cpuPercent': 0.11486798859431271, 'cpuTime': 7737.3999999999996}, 'system': {'cpuPercent': 1.4258630794508551, 'cpuTime': 96044.800000000003}, 'idle': {'cpuPercent': 94.031635591815515, 'cpuTime': 6333882.7999999998}, 'user': {'cpuPercent': 4.3198738234216778, 'cpuTime': 290982.65000000002}, 'irq': {'cpuPercent': 0.0503180995142802, 'cpuTime': 3389.3800000000001}, 'nice': {'cpuPercent': 0.053569777796624703, 'cpuTime': 3608.4099999999999}}
        self._cpuData = {
            'softirq'   : {'cpuPercent': 1.0,   'cpuTime': 12.12},
            'iowait'    : {'cpuPercent': 1.0,   'cpuTime': 12.12},
            'system'    : {'cpuPercent': 1.0,   'cpuTime': 12.12},
            'idle'      : {'cpuPercent': 90.0,  'cpuTime': 12.12},
            'user'      : {'cpuPercent': 5.0,   'cpuTime': 12.12},
            'irq'       : {'cpuPercent': 1.0,   'cpuTime': 12.12},
            'nice'      : {'cpuPercent': 1.0,   'cpuTime': 12.12}
            }
        self.assertEqual(myPlugin.computeOutput(), myPlugin._exitCodes['OK'])

        """
        sleepDurationMicroseconds = 1000	# No matter how long : the return value is a number of µs
        obj = modules.timer.Timer()
	obj.start()
        time.sleep(1.0 * sleepDurationMicroseconds / 1000000)	# expects seconds. "1.0 * ..." is a hack to convert to a float.
        sleepDuration = obj.stop()
        self.assertTrue((sleepDuration > sleepDurationMicroseconds) and (sleepDuration < (2 * sleepDurationMicroseconds)))
        """
#        self.assertTrue(True)
        

# uncomment this to run this unit test manually
if __name__ == '__main__':
    unittest.main()
