#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from ansible.plugins.callback import CallbackBase


class Play_book_callback(CallbackBase):
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super(Play_book_callback, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()] = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }
