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
#from modules import Debug

myUtility = Utility.Utility()


class test_Snmp(unittest.TestCase):

    def test1_get(self):
        """
        Given community, version, host, OID = '1.3.6.1.2.1.1.7.0'
        Should return 72
        """
        mySnmp = Snmp.Snmp(myUtility, host='192.168.1.101', community='public', version='2c')
        self.assertEqual(mySnmp.get('1.3.6.1.2.1.1.7.0'), 72)

#TESTING
#    def test2_get(self):
#        """
#        Given community, version, host, and a non-existing OID = '1.2.3.4'
#        Should return None
#        """
#        mySnmp = Snmp.Snmp(myUtility, host='192.168.1.101', community='public', version='2c')
#        self.assertEqual(mySnmp.get('1.2.3.4'), None)


#    def test3_get(self):
#        """
#        Given community, version, OID = '1.3.6.1.2.1.1.7.0' and an existing IP address with no SNMPd listening
#        Should return None
#        """
#        mySnmp = Snmp.Snmp(myUtility, host='10.20.30.40', community='public', version='2c')
#        self.assertEqual(mySnmp.get('1.3.6.1.2.1.1.7.0'), 72)


#    def test4_get(self):
#        """
#        Given community, version, OID = '1.3.6.1.2.1.1.7.0' and a non-existing IP address
#        Should return None
#        """
#        mySnmp = Snmp.Snmp(myUtility, host='123.456.789.987', community='public', version='2c')
#        self.assertEqual(mySnmp.get('1.3.6.1.2.1.1.7.0'), 72)


    def test1_walk(self):
        """
        Given community, version, host, OID = '1.3.6.1.2.1.1.9.1.2'
        Should return a dictionary which values all contain '1.3.6.1.'
        """
        import string

        mySnmp = Snmp.Snmp(myUtility, host='192.168.1.101', community='public', version='2c')
        result = mySnmp.walk('1.3.6.1.2.1.1.9.1.2')
        resultIsADict = True if isinstance(result, dict) else False

        valuesAreOk = True
        for value in result.values():
            try:
                string.index(value, '1.3.6.1.')
            except ValueError:
                valuesAreOk = False
        self.assertTrue(resultIsADict and valuesAreOk)
