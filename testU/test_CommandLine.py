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


from modules import CommandLine
from modules import Utility
from modules import Debug


class test_CommandLine(unittest.TestCase):

    def test1_validateArgs(self):
        """
        Given 2 valid arguments 'integer1' and 'integer2',
        Should return 'True'
        """
        integer1Value     = 12
#        integer1Value     = 'a'
        integer2Value    = 42
        integerRule     = '(\d+)'     

        myUtility       = Utility.Utility()
        myDebug         = Debug.Debug()

        myCommandLine   = CommandLine.CommandLine(
            description = 'Blah blah blah.',
            objDebug    = myDebug,
            objUtility  = myUtility
            )

        """
        self._argDict[argData['longOption']] = {
            'value'         : 0,
            'rule'          : argData['rule'],
            'orArgGroup'    : self._getOrArgGroup(argData)
            }
        myCommandLine._objDebug.enable(True)
        """
        myCommandLine._argDict['integer1'] = {
            'value'         : integer1Value,
            'rule'          : integerRule,
            'orArgGroup'    : 'aaa'
            }
        myCommandLine._argDict['integer2'] = {
            'value'         : integer2Value,
            'rule'          : integerRule,
            'orArgGroup'    : 'aaa'
            }

        self.assertEqual(myCommandLine._validateArgs(), True)


    def test2_validateArgs(self):
        """
        Given 1 valid and 1 invalid argument 'integer1' and 'integer2',
        Should return 'False'
        """
        integer1Value     = 12
        integer2Value     = 'a'
        integerRule     = '(\d+)'     

        myUtility       = Utility.Utility()
        myDebug         = Debug.Debug()

        myCommandLine   = CommandLine.CommandLine(
            description = 'Blah blah blah.',
            objDebug    = myDebug,
            objUtility  = myUtility
            )

        myCommandLine._argDict['integer1'] = {
            'value'         : integer1Value,
            'rule'          : integerRule,
            'orArgGroup'    : 'aaa'
            }
        myCommandLine._argDict['integer2'] = {
            'value'         : integer2Value,
            'rule'          : integerRule,
            'orArgGroup'    : 'aaa'
            }

        self.assertEqual(myCommandLine._validateArgs(), False)


    def test3_validateArgs(self):
        """
        Given 2 invalid arguments 'integer1' and 'integer2',
        Should return 'False'
        """
        integer1Value     = 12.34
        integer2Value     = 'a'
        integerRule     = '(\d+)'     

        myUtility       = Utility.Utility()
        myDebug         = Debug.Debug()

        myCommandLine   = CommandLine.CommandLine(
            description = 'Blah blah blah.',
            objDebug    = myDebug,
            objUtility  = myUtility
            )

        myCommandLine._argDict['integer1'] = {
            'value'         : integer1Value,
            'rule'          : integerRule,
            'orArgGroup'    : 'aaa'
            }
        myCommandLine._argDict['integer2'] = {
            'value'         : integer2Value,
            'rule'          : integerRule,
            'orArgGroup'    : 'aaa'
            }

        self.assertEqual(myCommandLine._validateArgs(), False)



        

# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
