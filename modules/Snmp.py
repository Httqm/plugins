#!/usr/bin/env python
# -*- coding: utf-8 -*-

# snmpwalk -On -c public -v 2c 192.168.1.101 1.3.6.1

#snmpget -On -c public -v 2c 192.168.1.101 1.3.6.1.2.1.1.7.0
# ==> .1.3.6.1.2.1.1.7.0 = INTEGER: 72


class Snmp(object):

    def __init__(self, community, version, host):
        """

        """

        pass


    def get(self, OID):
        """

        """
        return 72


    def walk(self, OID):
        """

        """
        pass

