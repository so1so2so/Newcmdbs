#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.inventory.host import Host, Group
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hosts_file = os.path.join(BASE_DIR, "hosts")
loader = DataLoader()  # 读取文件
Inventory = InventoryManager(loader=loader, sources=[hosts_file, ])  # 导入主机配置文件
Inventory.add_group('test_group')
my_group = Group(name='test_group')
my_group.set_variable(key="zhang",value="neng")

my_host = Host(name='192.168.1.11', port=22)
print my_host.get_vars()
