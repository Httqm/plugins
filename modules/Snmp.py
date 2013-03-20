#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SNMP GET :
#
# snmpget -On -c public -v 2c 192.168.1.101 1.3.6.1.2.1.1.7.0
#   ==> returns :
#   .1.3.6.1.2.1.1.7.0 = INTEGER: 72
#
#
# SNMP WALK :
#
# snmpwalk -On -c public -v 2c 192.168.1.101 1.3.6.1.2.1.1.9.1.4
#   ==> returns :
#   .1.3.6.1.2.1.1.9.1.4.1 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.2 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.3 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.4 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.5 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.6 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.7 = Timeticks: (40) 0:00:00.40
#   .1.3.6.1.2.1.1.9.1.4.8 = Timeticks: (40) 0:00:00.40

from pysnmp.entity.rfc3413.oneliner import cmdgen


class Snmp(object):

    def __init__(self, utility, host, community='public', version='2c'):
        self._utility = utility
        self._host = host
        self._community = community
        # TODO : version is unused

        self._cmdGen = cmdgen.CommandGenerator()


    def get(self, OID):
        """

        """
        errorIndication, errorStatus, errorIndex, varBinds = self._cmdGen.getCmd(
            cmdgen.CommunityData(self._community),
            cmdgen.UdpTransportTarget((self._host, 161)),
            OID
            )

        # Check for errors and print out results
        if errorIndication:
            print 'ERROR'
            print(errorIndication)
            # TODO : fix this
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex)-1] or '?'
                    )
                )
                # TODO : fix this
            else:
                for oid, value in varBinds:
                    try:
                        oidValue = value if self._utility.isNumber(value) else str(value)
                    except AttributeError:
                        # When the specified OID doesn't exist, 'value' doesn't either
                        oidValue = None

        return oidValue


    def walk(self, OID):
        """

        """
        returnData = {}
        errorIndication, errorStatus, errorIndex, varBindTable = self._cmdGen.nextCmd(
            cmdgen.CommunityData(self._community),
            cmdgen.UdpTransportTarget((self._host, 161)),
            OID,
            )

        if errorIndication:
            print(errorIndication)
            # TODO : don't print, 'except'
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
                # TODO : don't print, 'except'
            else:
                for varBindTableRow in varBindTable:
                    for oid, value in varBindTableRow:
#                        print('%s = %s' % (oid.prettyPrint(), value.prettyPrint()))
                        try:
                            returnData[oid] = value if self._utility.isNumber(value) else str(value)
                        except AttributeError:
                            # When the specified OID doesn't exist, 'value' doesn't either
                            returnData[oid] = None
#            print returnData
        return returnData
