#!/usr/bin/env python3
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
# snmpwalk -On -c public -v 2c 192.168.1.101 1.3.6.1.2.1.1.9.1.2
#   ==> returns :
#   .1.3.6.1.2.1.1.9.1.2.1 = OID: .1.3.6.1.6.3.10.3.1.1
#   .1.3.6.1.2.1.1.9.1.2.2 = OID: .1.3.6.1.6.3.11.3.1.1
#   .1.3.6.1.2.1.1.9.1.2.3 = OID: .1.3.6.1.6.3.15.2.1.1
#   .1.3.6.1.2.1.1.9.1.2.4 = OID: .1.3.6.1.6.3.1
#   .1.3.6.1.2.1.1.9.1.2.5 = OID: .1.3.6.1.2.1.49
#   .1.3.6.1.2.1.1.9.1.2.6 = OID: .1.3.6.1.2.1.4
#   .1.3.6.1.2.1.1.9.1.2.7 = OID: .1.3.6.1.2.1.50
#   .1.3.6.1.2.1.1.9.1.2.8 = OID: .1.3.6.1.6.3.16.2.2.1

# /usr/local/lib/python2.6/dist-packages/pysnmp/entity/rfc3413/oneliner/cmdgen.py
# /usr/local/lib/python3.1/dist-packages/pysnmp-4.2.5rc0-py3.1.egg/pysnmp
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto.rfc1905 import NoSuchObject


class Snmp(object):

    def __init__(self, utility, debug, host, port=161, community='public', version='2c', timeoutMilliseconds=1000):
        self._utility   = utility
        self._debug     = debug
        self._host = host
        self._port = port
        self._community = community
        # TODO : version is unused
        self._timeoutMilliseconds = timeoutMilliseconds
        self._cmdGen = cmdgen.CommandGenerator()


    def get(self, OID):
        try:
            errorIndication, errorStatus, errorIndex, varBinds = self._cmdGen.getCmd(
                cmdgen.CommunityData(self._community),

                # /usr/local/lib/python2.6/dist-packages/pysnmp/entity/rfc3413/oneliner/target.py
                cmdgen.UdpTransportTarget(
                    transportAddr = (self._host, self._port),
                    timeout = self._timeoutMilliseconds / 1000,
                    retries = 3
                    ),
                OID
                )
                # TODO : test the timeout + retries
        except Exception as e:    # this catches errors such as invalid IP
            self._debug.show('GET - ERROR 1 : %s' % e.args[0])
            return None


        if errorIndication: # Check for errors (such as timeouts) and print out results
            self._debug.show('GET - ERROR 2 : %s' % errorIndication)
            return None
        else:
            if errorStatus:
                self._debug.show('%s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex)-1] or '?'
                        )
                    )
                # TODO : don't print, 'except'

            else:

                # http://stackoverflow.com/questions/16178565/how-to-identify-a-nosuchobject-in-python
                if isinstance(varBinds[0][1], NoSuchObject):    # 'NoSuchObject' in returned tuple because of invalid OID
                    self._debug.show('GET - ERROR 3 : Invalid OID')
                    return None

                for oid, value in varBinds:
                    try:
                        oidValue = value if self._utility.isNumber(value) else str(value)
 
                    except AttributeError:
                        self._debug.show('GET - ERROR 3 : Invalid OID')
                        # When the specified OID doesn't exist, 'value' doesn't either
                        oidValue = None
        return oidValue


    def walk(self, OID):
        returnData = {}

        try:
            errorIndication, errorStatus, errorIndex, varBindTable = self._cmdGen.nextCmd(
                cmdgen.CommunityData(self._community),
                cmdgen.UdpTransportTarget((self._host, self._port)),
                OID,
                )
        except Exception as e:    # this catches errors such as invalid IP
            self._debug.show('WALK - ERROR 1 : %s' % e.args[0])
            return None

        if errorIndication:     # Check for errors (such as timeouts) and print out results
            self._debug.show('WALK - ERROR 2 : %s' % errorIndication)
            return None
        else:
            if errorStatus:
                self._debug.show('%s at %s' % (
                        errorStatus.prettyPrint(),
                        errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                        )
                    )
                # TODO : don't print, 'except'
            else:
                if not varBindTable:    # list is empty because of invalid OID
                    self._debug.show('WALK - ERROR 3 : Invalid OID')
                    return None

#                self._debug.show(varBindTable)

                for varBindTableRow in varBindTable:
                    for oid, value in varBindTableRow:
#                        self._debug.show('%s = %s' % (oid.prettyPrint(), value.prettyPrint()))
                        oid     = str(oid)
                        value   = str(value)
                        try:
                            returnData[oid] = float(value) if self._utility.isNumber(value) else value
                        except AttributeError:
                            # When the specified OID doesn't exist, 'value' doesn't either.
                            return None
#            self._debug.show(returnData)
        return returnData
