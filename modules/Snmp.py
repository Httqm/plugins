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
#                    print 'OID : ' + str(oid) + ', VALUE : ' + str(value)
                    try:
                        oidValue = value if self._utility.isNumber(value) else str(value)
                    except AttributeError:
                        # When the specified OID doesn't exist, 'value' doesn't either
                        oidValue = None

#            print oidValue
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
        else:
            if errorStatus:
                print('%s at %s' % (
                    errorStatus.prettyPrint(),
                    errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                    )
                )
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
























# source : http://pysnmp.sourceforge.net/examples/current/v1arch/manager/getgen.html

from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import encoder, decoder
from pysnmp.proto import api
from time import time


class Snmp2(object):

    def __init__(self, utility, host, community='public', version='2c', timeoutSeconds=3):
        """

        """
        self._return = {}
        self._host = host
        self._community = community
        self._timeoutSeconds = timeoutSeconds
        self._utility = utility

        # Protocol version to use
        defaultSnmpVersion = api.protoModules[api.protoVersion2c]
        # {'a': 1, 'b': 2,}.get('a', 9)
        # source : http://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
        self._protocolModule = {
            '1'  : api.protoModules[api.protoVersion1],
            '2c' : api.protoModules[api.protoVersion2c]
            }.get(version, defaultSnmpVersion)


    def get(self, OID):
        """

        """
        self._OID = OID
	self._buildPDU()
	self._buildMessage()
	self._startTime = time()
        self._send()
        return self._return[self._OID]


    def walk(self, OID):
        """

        """
        self._OID = OID
        return {}


    def _buildPDU(self):
        """
        PDU (Protocol Data unit) are complex data types specific to SNMP. The PDU field contains the body of an SNMP message.
        """
        self._requestPDU =  self._protocolModule.GetRequestPDU()
        self._protocolModule.apiPDU.setDefaults(self._requestPDU)
        self._protocolModule.apiPDU.setVarBinds(
            self._requestPDU, (
                (self._OID, self._protocolModule.Null('')),
                )
            )
        """
        Unit testing this fails miserably without the final ',' :
            ValueError: too many values to unpack
        ==> WTFF?!?
        """


    def _buildMessage(self):
        self._requestMessage = self._protocolModule.Message()
        self._protocolModule.apiMessage.setDefaults(self._requestMessage)
        self._protocolModule.apiMessage.setCommunity(self._requestMessage, self._community)
        self._protocolModule.apiMessage.setPDU(self._requestMessage, self._requestPDU)


    def _timer(self, timeNow):
        if timeNow - self._startTime > self._timeoutSeconds:
            raise Exception('Request timed out')


    def _receive(self, unusedArg, transportDomain, transportAddress, wholeMsg): #TODO : fix the number of args question
        """
        As stated by its name, 'unusedArg' is not used ;-)
        Without it, this function, called by /usr/local/lib/python2.6/dist-packages/pysnmp/carrier/base.py fails :
        File "/usr/local/lib/python2.6/dist-packages/pysnmp/carrier/base.py", line 44, in _cbFun
            self, transportDomain, transportAddress, incomingMessage
        TypeError: _receive() takes exactly 4 arguments (5 given)
        """
        while wholeMsg:
            responseMessage, wholeMsg = decoder.decode(wholeMsg, asn1Spec=self._protocolModule.Message())
            responsePDU = self._protocolModule.apiMessage.getPDU(responseMessage)
            # Match response to request
            if self._protocolModule.apiPDU.getRequestID(self._requestPDU) == self._protocolModule.apiPDU.getRequestID(responsePDU):
                # Check for SNMP errors reported
                errorStatus = self._protocolModule.apiPDU.getErrorStatus(responsePDU)
                if errorStatus:
                    print(errorStatus.prettyPrint())
                else:
                    for oid, value in self._protocolModule.apiPDU.getVarBinds(responsePDU):
#                        print('%s = %s' % (oid.prettyPrint(), value.prettyPrint()))
                        try:
                            self._return[str(oid)] = value if self._utility.isNumber(value) else str(value)
                        except AttributeError:
                            # When the specified OID doesn't exist, 'value' doesn't either
                            self._return[str(oid)] = None
                self._transportDispatcher.jobFinished(1)
        return wholeMsg


    def _send(self):
        self._transportDispatcher = AsynsockDispatcher()

        # transport on UDP/IPv4
        self._transportDispatcher.registerRecvCbFun(self._receive)
        self._transportDispatcher.registerTimerCbFun(self._timer)

        self._transportDispatcher.registerTransport(
            udp.domainName,
            udp.UdpSocketTransport().openClientMode()
            )

        # Pass message to dispatcher
        self._transportDispatcher.sendMessage(
            encoder.encode(self._requestMessage),
            udp.domainName, (self._host, 161)
            )
        self._transportDispatcher.jobStarted(1)

        # Dispatcher will finish as job#1 counter reaches zero
        self._transportDispatcher.runDispatcher()

        self._transportDispatcher.closeDispatcher()
