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


import modules.Utility as Utility


class test_Utility(unittest.TestCase):

    def test1_computePercentage(self):
        """
        Given a number and a total (both are >0)
	should return a percentage (float) : 0 <= number <= 100
        """
        myUtility   = Utility.Utility()
        number      = 12
        total       = 42
        percentage  = myUtility.computePercentage(number, total)
        self.assertTrue((percentage >= 0) and (percentage <= 100))


    def test2_computePercentage(self):
        """
        Given any number and total == 0
	should return 0
        """
        myUtility   = Utility.Utility()
        number      = 12
        total       = 0
        expected    = 0
        self.assertEqual(myUtility.computePercentage(number, total), expected)


# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
