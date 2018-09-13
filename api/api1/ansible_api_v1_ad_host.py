#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from callback import MyCallbackBase

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hosts_file = os.path.join(BASE_DIR, "hosts")
# print hosts_file

loader = DataLoader()  # 读取文件
inv = InventoryManager(loader=loader, sources=[hosts_file, ])  # 导入主机配置文件
onehost = inv.get_host('192.168.1.11')
inv.add_host(host='192.168.1.100', port=10022, group='k8s')
# print inv.get_groups_dict()
Variable = VariableManager(loader=loader, inventory=inv)  # 存储变量信息
# print Variable.get_vars()
# print Variable.get_vars(host=onehost)
# Variable.set_host_variable(host=onehost,varname='test',value='654123')
Variable.extra_vars = {'myweb': 'test1', 'username': 'zhangneng'}
# print Variable.get_vars()
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                 'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                 'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                 'verbosity', 'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])
options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                  remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                  sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                  become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                  listtasks=False, listtags=False, syntax=False, diff=True)
# options 存储执行选项

# play 存储执行对象
play_source = dict(
    name="Ansible Play",
    hosts='192.168.1.11',
    gather_facts='no',  # 执行前setup是否使用
    tasks=[dict(action=dict(module='shell', args='cd  /tmp/api1.txt')),
           # dict(action=dict(module='shell', args="mkdir /tmp/1/2/3/34/4 -p")),
           ]
)

# play_source = {'gather_facts': 'no', 'tasks': [{'action': {'args': 'ls /tmp', 'module': 'shell'}}],
#                'hosts': '192.168.1.11', 'name': 'Ansible Play'}
play = Play().load(data=play_source, variable_manager=Variable, loader=loader)  # 创建执行对象

passwords = dict()
callback = MyCallbackBase()
tqm = TaskQueueManager(
    inventory=inv,
    variable_manager=Variable,
    loader=loader,
    options=options,
    passwords=passwords,
    stdout_callback=callback,
)
# tqm 执行队列加入执行的对象
result = tqm.run(play)  # 执行队列

# print type(callback.host_ok)
# print callback.host_ok
all_result = {
    'success': {},
    'failed': {},
    'unreachable': {},

}

import json
for host, result in callback.host_ok.items():
    all_result['success'][host] = result._result
for host, result in callback.host_failed.items():
    all_result['failed'][host] = result._result
for host, result in callback.host_unreachable.items():
    all_result['unreachable'][host] = result._result
print json.dumps(all_result,ensure_ascii=False)
