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


import modules.timer
import time

class test_Timer(unittest.TestCase):

    def test1_stop(self):
        """
        Given a timer instance,
	should return an integer.
        """
        sleepDurationMicroseconds = 1000	# No matter how long : the return value is a number of µs
        obj = modules.timer.Timer()
	obj.start()
        time.sleep(1.0 * sleepDurationMicroseconds / 1000000)	# expects seconds. "1.0 * ..." is a hack to convert to a float.
        sleepDuration = obj.stop()
        self.assertTrue((sleepDuration > sleepDurationMicroseconds) and (sleepDuration < (2 * sleepDurationMicroseconds)))


if __name__ == '__main__':
    unittest.main()
