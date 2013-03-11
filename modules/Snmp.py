#!/usr/bin/env python
# -*- coding: utf-8 -*-

# snmpwalk -On -c public -v 2c 192.168.1.101 1.3.6.1

#snmpget -On -c public -v 2c 192.168.1.101 1.3.6.1.2.1.1.7.0
# ==> .1.3.6.1.2.1.1.7.0 = INTEGER: 72



# source : http://pysnmp.sourceforge.net/examples/current/v1arch/manager/getgen.html

from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
from time import time


class Snmp(object):

    def __init__(self, community, version, host):
        """

        """

        # Protocol version to use
        #pMod = api.protoModules[api.protoVersion1]
        #pMod = api.protoModules[api.protoVersion2c]

        # {'a': 1, 'b': 2,}.get('a', 9)
        # source : http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
        #version = '2'
        defaultSnmpVersion = api.protoModules[api.protoVersion2c]
        pMod = {
            '1'  : api.protoModules[api.protoVersion1],
            '2c' : api.protoModules[api.protoVersion2c]
            }.get(version, defaultSnmpVersion)

        print pMod
        pass


    def get(self, OID):
        """

        """
        return 72


    def walk(self, OID):
        """

        """
        pass

