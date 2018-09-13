#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager

from ansible.executor.playbook_executor import PlaybookExecutor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
hosts_file = os.path.join(BASE_DIR, "hosts")
playbook_path = os.path.join(BASE_DIR, "first.yaml")
Loader = DataLoader()  # 读取文件
Inventory = InventoryManager(loader=Loader, sources=[hosts_file, ])  # 导入主机配置文件
Variable = VariableManager(loader=Loader, inventory=Inventory)  # 存储变量信息
# options 存储执行选项
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                 'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user',
                                 'ask_value_pass', 'verbosity', 'check', 'listhosts', 'listtasks', 'listtags', 'syntax',
                                 'diff'])
options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                  remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                  sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                  become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                  listtasks=False, listtags=False, syntax=False, diff=True)
# Playbook 方式执行
passwords = dict()
# 创建playbook对象
playbook = PlaybookExecutor(
    playbooks=[playbook_path, ], inventory=Inventory, variable_manager=Variable, loader=Loader,
    options=options, passwords=passwords,
)
from callback import PlayBookResultsCollector

callback = PlayBookResultsCollector()
playbook._tqm._stdout_callback = callback
playbook.run()
all_result = {
    'success': {},
    'failed': {},
    'unreachable': {},
    'skipped': {},
    'status': {},

}
# print callback.task_status
import json

for host, result in callback.task_ok.items():
    all_result['success'][host] = result._result
for host, result in callback.task_failed.items():
    all_result['failed'][host] = result._result
for host, result in callback.task_unreachable.items():
    all_result['unreachable'][host] = result._result
for host, result in callback.task_skipped.items():
    all_result['skipped'][host] = result._result
for host, result in callback.task_status.items():
    all_result['status'][host] = result
print json.dumps(all_result, ensure_ascii=False)
