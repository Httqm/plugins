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
#from modules import Utility
#from modules import Debug


class test_Snmp(unittest.TestCase):

    def test_get(self):
        """
        Given community, version, host, OID
        Should return 72
        """
        mySnmp = Snmp.Snmp(host='192.168.1.101', community='public', version='2c')
        
        self.assertEqual(mySnmp.get('1.3.6.1.2.1.1.7.0'), '72')

