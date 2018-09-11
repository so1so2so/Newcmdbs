#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import nmap

nmScan = nmap.PortScanner()
f= nmScan.scan('192.168.1.0/24', arguments="-n -sP -PE")

print f
all_host=nmScan.all_hosts()

# # {u'tcp': {'services': u'20-443', 'method': u'syn'}}
# print nmScan.command_line()
# # u'nmap -oX - -p 20-443 -sV 115.239.210.26'
