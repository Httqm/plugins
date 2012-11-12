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

    def test1_checkArgsMatchRules(self):
        """
        Given 2 valid arguments 'integer1' and 'integer2',
        Should return 'True'
        """
        integer1Value     = 12
        integer2Value    = 42
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
            }
        myCommandLine._argDict['integer2'] = {
            'value'         : integer2Value,
            'rule'          : integerRule,
            }

        self.assertEqual(myCommandLine.checkArgsMatchRules(), True)


    def test2_checkArgsMatchRules(self):
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
            }
        myCommandLine._argDict['integer2'] = {
            'value'         : integer2Value,
            'rule'          : integerRule,
            }

        self.assertEqual(myCommandLine.checkArgsMatchRules(), False)


    def test3_checkArgsMatchRules(self):
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
            }
        myCommandLine._argDict['integer2'] = {
            'value'         : integer2Value,
            'rule'          : integerRule,
            }

        self.assertEqual(myCommandLine.checkArgsMatchRules(), False)


    def test1_checkOrArgGroups(self):
        """
        Given 2 arguments while expecting 2 'orArg' arguments in a single group,
        Should return 'True' and an empty message
        """
        myUtility       = Utility.Utility()
        myDebug         = Debug.Debug()

        myCommandLine   = CommandLine.CommandLine(
            description = 'Blah blah blah.',
            objDebug    = myDebug,
            objUtility  = myUtility
            )

        myCommandLine._argDict['arg1'] = {
            'value'         : 'blah',
            'orArgGroup'    : 'group1'
            }

        myCommandLine._argDict['arg2'] = {
            'value'         : 'meh',
            'orArgGroup'    : 'group1'
            }

        orArgsAreOk, message = myCommandLine.checkOrArgGroups()
        self.assertTrue(orArgsAreOk)
        self.assertEqual(message, '')


    def test2_checkOrArgGroups(self):
        """
        Given 1 argument while expecting 2 'orArg' arguments in a single group,
        Should return 'True' and an empty message
        """
        myUtility       = Utility.Utility()
        myDebug         = Debug.Debug()

        myCommandLine   = CommandLine.CommandLine(
            description = 'Blah blah blah.',
            objDebug    = myDebug,
            objUtility  = myUtility
            )

        myCommandLine._argDict['arg1'] = {
            'value'         : 'blah',
            'orArgGroup'    : 'group1'
            }

        myCommandLine._argDict['arg2'] = {
            'value'         : None,
            'orArgGroup'    : 'group1'
            }

        orArgsAreOk, message = myCommandLine.checkOrArgGroups()
        self.assertTrue(orArgsAreOk)
        self.assertEqual(message, '')


    def test3_checkOrArgGroups(self):
        """
        Given no argument while expecting 2 'orArg' arguments in a single group,
        Should return 'False' and an error message
        """
        myUtility       = Utility.Utility()
        myDebug         = Debug.Debug()

        myCommandLine   = CommandLine.CommandLine(
            description = 'Blah blah blah.',
            objDebug    = myDebug,
            objUtility  = myUtility
            )

        myCommandLine._argDict['arg1'] = {
            'value'         : None,
            'orArgGroup'    : 'group1'
            }

        myCommandLine._argDict['arg2'] = {
            'value'         : None,
            'orArgGroup'    : 'group1'
            }

        orArgsAreOk, message = myCommandLine.checkOrArgGroups()
        self.assertFalse(orArgsAreOk)
        self.assertNotEqual(message, '')


# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
