#!/usr/bin/env python

import unittest


########################################## ##########################################################
# allows importing from parent folder
# source : http://stackoverflow.com/questions/714063/python-importing-modules-from-parent-folder
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
########################################## ##########################################################



"""
import os, sys, inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subforder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

# Info:
# cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
# __file__ fails if script is called in different ways on Windows
# __file__ fails if someone does os.chdir() before
# sys.argv[0] also fails because it doesn't not always contains the path
"""



import modules.url

class test_Url(unittest.TestCase):

    def test_getFullUrl_case1(self):
        testUrl = 'http://www.google.be'
        obj     = modules.url.Url(full=testUrl)
        self.assertEqual(obj.getFullUrl(), testUrl)
#        self.assertTrue(obj.returnTrue())


#    def test_returnTrue_case2(self):
#        obj = programm.MaClasse()
#        self.assertNotEqual(obj.returnTrue(), False)


if __name__ == '__main__':
    unittest.main()
