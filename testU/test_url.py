#!/usr/bin/env python

import unittest

########################################## ##########################################################
# allows importing from parent folder
# source : http://stackoverflow.com/questions/714063/python-importing-modules-from-parent-folder
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
########################################## ##########################################################


import modules.url

class test_Url(unittest.TestCase):

    def test1_getFullUrl(self):
        """
        Given a URL,
        should return the full URL.
        """
        testUrl = 'http://www.google.be'
        obj     = modules.url.Url(full=testUrl)
        self.assertEqual(obj.getFullUrl(), testUrl)


    def test1_getQuery(self):
        """
        Given a short URL,
        should return its 'HTTP query' part.
        """
        testUrl     = 'http://www.google.be'
        obj         = modules.url.Url(full=testUrl)
        self.assertEqual(obj.getQuery(), '/')


    def test2_getQuery(self):
        """
        Given a long URL,
        should return its 'HTTP query' part.
        """
        testQuery   = '/index.php'
        testUrl     = 'http://www.bla.com' + testQuery
        obj         = modules.url.Url(full=testUrl)
        self.assertEqual(obj.getQuery(), testQuery)


    def test1_getHostName(self):
        """
        Given a 'legal' URL,
        should return its "hostname" part.
        """
        testHostName    = 'www.thisisnot.net'
        testUrl         = 'http://' + testHostName + '/myPage.php'
        obj             = modules.url.Url(full=testUrl)
        self.assertEqual(obj.getHostName(), testHostName)


    def test2_getHostName(self):
        """
        Given a wrong URL,
        should return the full URL.
        """
        testUrl         = 'thisisawrongurl.com'
        obj             = modules.url.Url(full=testUrl)
        self.assertEqual(obj.getHostName(), testUrl)


# uncomment this to run this unit test manually
#if __name__ == '__main__':
#    unittest.main()
