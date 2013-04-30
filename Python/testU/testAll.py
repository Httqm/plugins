#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run all unit tests of all "test_*.py" files.
Source : http://stackoverflow.com/questions/1732438/run-all-unit-test-in-python-directory/1735277#1735277
"""

import glob
import unittest


test_file_strings   = glob.glob('test_*.py')
module_strings      = [str[0:len(str)-3] for str in test_file_strings]
suites              = [unittest.defaultTestLoader.loadTestsFromName(str) for str in module_strings]
testSuite           = unittest.TestSuite(suites)
text_runner         = unittest.TextTestRunner().run(testSuite)
