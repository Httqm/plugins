#!/usr/bin/env python3
# source : http://pysnmp.sourceforge.net/examples/current/v3arch/oneliner/manager/cmdgen/get-v2c.html

# snmpget -v2c -c public -ObentU 192.168.1.101 1.3.6.1.2.1.1.7.0


from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('192.168.1.101', 161)),
    '1.3.6.1.2.1.1.7.0'
#    ,
#    '1.3.6.1.2.1.1.6.0'
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
