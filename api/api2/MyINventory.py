#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.inventory.host import Host, Group

BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
print '%s/conf/hosts' % BASE_DIR


class MyInventory():
    """
    this is IOPS ansible inventory object.
    """

    # myinvent = MyInventory(self.resource, self.loader, self.variable_manager)
    def __init__(self, resource, loader, variable_manager):
        self.resource = resource
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=['%s/conf/hosts' % BASE_DIR])
        # self.variable_manager.set_inventory(self.inventory)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        # 自动执行dynamic_inventory
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        """
            add hosts to a group
        """

        self.inventory.add_group(groupname)
        my_group = Group(name=groupname)

        # if group variables exists, add them to group if dict
        # groupvars={'var1': 'ansible', 'var2': 'saltstack'}
        if groupvars:
            for key, value in groupvars.iteritems():
                my_group.set_variable(key, value)
# if list hosts=resource [{"hostname": "192.168.1.111"}], if dict host=[{'username': u'root', 'ip': '192.168.1.11',}]
        # add hosts to group,all hosts is list
        for host in hosts:
            # set connection variables
            hostname = host.get("hostname")
            # 拿IP  没有IP就用hostname代替,没有IP一般是新增的
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_host', value=hostip)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_pass', value=password)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_port', value=hostport)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_user', value=username)
            self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_private_key_file', value=ssh_key)
            # my_host.set_variable('ansible_ssh_pass', password)
            # my_host.set_variable('ansible_ssh_private_key_file', ssh_key)

            # set other variables
            for key, value in host.iteritems():
                if key not in ["hostname", "port", "username", "password"]:
                    self.variable_manager.set_host_variable(host=my_host, varname=key, value=value)

            # add to group

            self.inventory.add_host(host=hostname, group=groupname, port=hostport)
            ghost = Host(name="192.168.8.119")

    def dynamic_inventory(self):
        """
            add hosts to inventory.
        """
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.iteritems():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


resource_list = [
    {"hostname": "192.168.1.111"},
    {"hostname": "192.168.6.43"},
    {"hostname": "192.168.1.233"},
]

groupname_list = 'default_group'
groupname2 = "dynamic_host"

hosts_and_vars = {
    "hosts": [
        {'username': u'root', 'password': '123456', 'ip': '192.168.1.11', 'hostname': 'nginx01', 'port': '22'},
        {"hostname": "778da6afsdwf", "ip": "192.168.1.109", "port": "22", "username": "root", "password": "123456"},
    ],
    "vars": {
        "var1": "ansible",
        "var2": "saltstack"
    }
}
hosts_and_vars_get_host = [
    {'username': u'root', 'ip': '192.168.1.11', 'password': '123456', 'hostname': 'nginx01', 'port': '22'},
    {'username': 'root', 'ip': '192.168.1.109', 'password': '123456', 'hostname': '778da6afsdwf', 'port': '22'}]
hosts_and_vars_get_vars = {'var1': 'ansible', 'var2': 'saltstack'}
resource = {
    "dynamic_host": {
        "hosts": [
            {'username': u'root', 'password': '123456', 'ip': '192.168.1.11', 'hostname': 'nginx01', 'port': '22'},
            {"hostname": "778da6afsdwf", "ip": "192.168.1.109", "port": "22", "username": "root", "password": "123456"},
        ],
        "vars": {
            "var1": "ansible",
            "var2": "saltstack"
        }
    }
}
