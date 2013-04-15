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


from modules import Snmp
from modules import Utility
from modules import Debug

myUtility   = Utility.Utility()
myDebug     = Debug.Debug()

#myDebug.enable(True)
myDebug.enable(False)

# test variables
testHostIp          = '192.168.1.101'
testHostPort        = 161
testHostCommunity   = 'public'
testHostVersion     = '2c'
unusedIpAddress     = '192.168.42.42'
invalidIpAddress    = '123.456.789.876'
invalidOid          = '2.3.4.5.6.7.8'

class test_Snmp(unittest.TestCase):

    def test1_get(self):
        """
        Given community, version, host, OID = '1.3.6.1.2.1.1.7.0'
        Should return 72
        """
        mySnmp = Snmp.Snmp(
            myUtility,
            myDebug,
            host    = testHostIp,
            port    = testHostPort,
            community   = testHostCommunity,
            version     = testHostVersion,
            timeoutMilliseconds = 1000
            )
        self.assertEqual(mySnmp.get('1.3.6.1.2.1.1.7.0'), 72)


    def test2_get(self):
        """
        Given community, version, host, and a non-existing OID
        Should return None
        """
        myDebug.show('This test MUST end on an "Invalid OID" error.')
        mySnmp = Snmp.Snmp(
            myUtility,
            myDebug,
            host    = testHostIp,
            port    = testHostPort,
            community   = testHostCommunity,
            version     = testHostVersion,
            timeoutMilliseconds = 1000
            )
        self.assertEqual(mySnmp.get(invalidOid), None)


    def test1_walk(self):
        """
        Given community, version, host, OID = '1.3.6.1.2.1.1.9.1.2'
        Should return a dictionary which values all contain '1.3.6.1.'
        """
        import string

        mySnmp = Snmp.Snmp(
            myUtility,
            myDebug,
            host    = testHostIp,
            port    = testHostPort,
            community   = testHostCommunity,
            version     = testHostVersion,
            timeoutMilliseconds = 1000
            )
        result = mySnmp.walk('1.3.6.1.2.1.1.9.1.2')
        resultIsADict = True if isinstance(result, dict) else False

        valuesAreOk = True
        for value in result.values():
            try:
                string.index(value, '1.3.6.1.')
            except ValueError:
                valuesAreOk = False
        self.assertTrue(resultIsADict and valuesAreOk)


    def test2_walk(self):
        """
        Given community, version, OID = '1.3.6.1.2.1.1.9.1.2' and an invalid IP address
        Should return None
        """
        myDebug.show('This test MUST end on a "Bad IPv4/UDP transport address" error.')
        mySnmp = Snmp.Snmp(
            myUtility,
            myDebug,
            host    = invalidIpAddress,
            port    = testHostPort,
            community   = testHostCommunity,
            version     = testHostVersion,
            timeoutMilliseconds = 1000
            )
        self.assertEqual(mySnmp.walk('1.3.6.1.2.1.1.9.1.2'), None)


    def test4_walk(self):
        """
        Given host, community, version, and an invalid OID
        Should return None
        """
        myDebug.show('This test MUST end on a "Invalid OID" error.')
        mySnmp = Snmp.Snmp(
            myUtility,
            myDebug,
            host    = testHostIp,
            port    = testHostPort,
            community   = testHostCommunity,
            version     = testHostVersion,
            timeoutMilliseconds = 1000
            )
        self.assertEqual(mySnmp.walk(invalidOid), None)






# Other tests not working for current Python version

    # 'skip' requires Python >= 2.7
    # http://docs.python.org/2/library/unittest.html#unittest-skipping
    # @unittest.skip("Don't want to wait for timeout : skipping this test !")
#    def test2_get(self):
#        """
#        Given community, version, OID = '1.3.6.1', and an address not used on the LAN
#        Should return None
#        """
#        mySnmp = Snmp.Snmp(myUtility, host=unusedIpAddress, community=testHostCommunity, version=testHostVersion, timeoutMilliseconds=1)
#        self.assertEqual(mySnmp.get('1.3.6.1'), None)
        #self.assertIsNone(mySnmp.get('1.3.6.1'))   # Requires Python >= 2.7
        # http://docs.python.org/2/library/unittest.html#assert-methods




    # 'skip' requires Python >= 2.7
    # http://docs.python.org/2/library/unittest.html#unittest-skipping
    # @unittest.skip("Don't want to wait for timeout : skipping this test !")
#    def test4_get(self):
#        """
#        Given community, version, OID = '1.3.6.1.2.1.1.7.0' and a non-existing IP address
#        Should return None
#        """
#        mySnmp = Snmp.Snmp(myUtility, host=invalidIpAddress, community=testHostCommunity, version=testHostVersion)
#        self.assertEqual(mySnmp.get('1.3.6.1.2.1.1.7.0'), None)




    # 'skip' requires Python >= 2.7
    # http://docs.python.org/2/library/unittest.html#unittest-skipping
    # @unittest.skip("Don't want to wait for timeout : skipping this test !")
#    def test2_walk(self):
#        """
#        Given community, version, OID = '1.3.6.1.2.1.1.9.1.2' and an unused IP address
#        Should return None
#        """
#        mySnmp = Snmp.Snmp(myUtility, host=unusedIpAddress, community=testHostCommunity, version=testHostVersion)
#        self.assertEqual(mySnmp.walk('1.3.6.1.2.1.1.9.1.2'), None)
