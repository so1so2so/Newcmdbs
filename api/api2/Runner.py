#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from MyINventory import MyInventory
from ansible.playbook.play import Play
from Mycallback.host_callback import Host_callback
from ansible.executor.task_queue_manager import TaskQueueManager
from Mycallback.playbook_callback import Play_book_callback
from ansible.executor.playbook_executor import PlaybookExecutor
import json
import os
BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
yaml_path= '%s/conf/first.yaml' % BASE_DIR
class ANSRunner(object):
    """
    This is a General object for parallel execute modules.
    """

    def __init__(self, resource, redisKey=None, logId=None, *args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        # 创建对象自动初始化
        self.__initializeData()
        self.results_raw = {}
        self.redisKey = redisKey
        self.logId = logId

    def __initializeData(self):
        """ 初始化ansible """
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout', 'remote_user',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax', 'diff'])

        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                               remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                               become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False, diff=True)

        self.passwords = dict(sshpass=None, becomepass=None)
        myinvent = MyInventory(self.resource, self.loader, self.variable_manager)
            # 添加自己的变量进去
        self.inventory = myinvent.inventory
        self.variable_manager = myinvent.variable_manager

        # self.variable_manager.set_inventory(self.inventory)
        # self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def run_model(self, host_list, module_name, module_args):
        """
        run module from andible ad-hoc.
        module_name: ansible module_name
        module_args: ansible module args
        """
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        # if self.redisKey:self.callback = ModelResultsCollectorToSave(self.redisKey,self.logId)
        # else:self.callback = ModelResultsCollector()
        self.callback = Host_callback()
        import traceback
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback="minimal",
            )
            tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
            tqm.run(play)
        except Exception as err:
            print traceback.print_exc()
            # DsRedis.OpsAnsibleModel.lpush(self.redisKey,data=err)
            # if self.logId:AnsibleSaveResult.Model.insert(self.logId, err)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, playbook_path, extra_vars=None):
        """
        run ansible palybook
        """
        try:
            # if self.redisKey:self.callback = PlayBookResultsCollectorToSave(self.redisKey,self.logId)
            self.callback = Play_book_callback()
            if extra_vars: self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            constants.HOST_KEY_CHECKING = False  # 关闭第一次使用ansible连接客户端是输入命令
            executor.run()
        except Exception as err:
            return False

    def get_model_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['success'][hostvisiable] = result._result

        for host, result in self.callback.host_failed.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['failed'][hostvisiable] = result._result

        for host, result in self.callback.host_unreachable.items():
            hostvisiable = host.replace('.', '_')
            self.results_raw['unreachable'][hostvisiable] = result._result

        return json.dumps(self.results_raw)
        # return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}, "changed": {}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result._result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        # for host, result in self.callback.task_changed.items():
        #     self.results_raw['changed'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result._result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return json.dumps(self.results_raw)


if __name__ == '__main__':
    resource1 = [
        {"hostname": "192.168.1.50","password":123456},
        {"hostname": "192.168.1.30","password":123456},
        {"hostname": "192.168.1.31","password":123456},
        # {"hostname": "192.168.6.43"},
        # {"hostname": "192.168.1.233"},
    ]
    resource2 = {
        "dynamic_host": {
            "hosts": [
                {'username': "root", 'password': 123456, 'ip': '192.168.1.30', 'hostname': 'study', 'port': 10022},
                {'username': "root", 'password': "123456", 'ip': '192.168.1.52', 'hostname': 'docker-client2 ', 'port': 22},
            ],
            "vars": {
                "var1": "ansible",
                "var2": "saltstack"
            }
        }
    }
    # myinvent = MyInventory(self.resource, self.loader, self.variable_manager)
    # rbt = ANSRunner(resource, redisKey='1')
    # rbt = ANSRunner(resource1)
    # # Ansible Adhoc
    # rbt.run_model(host_list=['test1','default_group'], module_name='shell', module_args="ls /root")
    # data = rbt.get_model_result()
    # print data
    # Ansible playbook
    rbt = ANSRunner(resource2)
    rbt.run_playbook(playbook_path=yaml_path)
    print rbt.get_playbook_result()
    # rbt.run_model(host_list=[],module_name='yum',module_args="name=htop state=present")
