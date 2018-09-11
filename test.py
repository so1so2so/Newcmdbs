#!/usr/bin/env python
# _*_ coding:utf-8 _*_

# from pysnmp.entity.rfc3413.oneliner import cmdgen
#
# cg = cmdgen.CommandGenerator()
# cg.getCmd(cmdgen.CommunityData('', 'public', 0),
#           cmdgen.UdpTransportTarget(('192.168.1.50', 161)),
#           'SNMPv2-MIB')
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    getCmd(SnmpEngine(),
           CommunityData('public', mpModel=0),
           UdpTransportTarget(('192.168.1.50', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
)
# print varBinds
if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))