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


#import modules.NagiosPlugin as NagiosPlugin
from modules import NagiosPlugin
from modules import Debug

class test_NagiosPlugin(unittest.TestCase):

    def test1_computeExitStatus(self):
        """
        Given 3 values : metric < warn < crit,
	should return 'OK'
        """
        myDebug = Debug.Debug()
        myPlugin = NagiosPlugin.NagiosPlugin(
            name        = 'bla',
            objDebug    = myDebug
            )
        self.assertEqual(myPlugin.computeExitStatus(1, 2, 3), 'OK')


    def test2_computeExitStatus(self):
        """
        Given 3 values : warn < metric < crit,
	should return 'WARNING'
        """
        myDebug = Debug.Debug()
        myPlugin = NagiosPlugin.NagiosPlugin(
            name        = 'bla',
            objDebug    = myDebug
            )
        self.assertEqual(myPlugin.computeExitStatus(2, 1, 3), 'WARNING')


    def test3_computeExitStatus(self):
        """
        Given 3 values : warn < crit < metric
	should return 'CRITICAL'
        """
        myDebug = Debug.Debug()
        myPlugin = NagiosPlugin.NagiosPlugin(
            name        = 'bla',
            objDebug    = myDebug
            )
        self.assertEqual(myPlugin.computeExitStatus(3, 1, 2), 'CRITICAL')


    def test4_computeExitStatus(self):
        """
        Given 3 values : crit < warn < metric
	should return 'OK'
        """
        myDebug = Debug.Debug()
        myPlugin = NagiosPlugin.NagiosPlugin(
            name        = 'bla',
            objDebug    = myDebug
            )
        self.assertEqual(myPlugin.computeExitStatus(3, 2, 1), 'OK')


    def test5_computeExitStatus(self):
        """
        Given 3 values : crit < metric < warn
	should return 'WARNING'
        """
        myDebug = Debug.Debug()
        myPlugin = NagiosPlugin.NagiosPlugin(
            name        = 'bla',
            objDebug    = myDebug
            )
        self.assertEqual(myPlugin.computeExitStatus(2, 3, 1), 'WARNING')


    def test6_computeExitStatus(self):
        """
        Given 3 values : metric < crit < warn
	should return 'CRITICAL'
        """
        myDebug = Debug.Debug()
        myPlugin = NagiosPlugin.NagiosPlugin(
            name        = 'bla',
            objDebug    = myDebug
            )
        self.assertEqual(myPlugin.computeExitStatus(1, 3, 2), 'CRITICAL')


# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
