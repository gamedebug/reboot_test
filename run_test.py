#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cases import TestCase
import os
import sys
import time
import json
import platform

# 初始化相关变量。
current_dir = sys.path[0]
rec = json.load(open(current_dir+'/etc/config.json'))
results_dir = current_dir+'/'+str(rec['results'])
time_file = results_dir+'/'+str(rec['time_list'])
boot_log = str(rec['boot_log'])
nic_list = str(rec['nic_list'])
test_report = str(rec['test_report'])
test_script = current_dir+'/'+str(rec['test_script'])
duration = str(float(rec['duration']))

# 判断操作系统发行版。
if platform.dist()[0] == 'redhat':
    auto_exec = str(rec['rh_auto_exec'])
elif platform.dist()[0] == 'SuSE':
    auto_exec = str(rec['su_auto_exec'])
else:
    raise Exception

# 为本次测试生成时间记录文件。
if os.path.exists(time_file):
    pass
else:
    TestCase().test_init(results_dir, time_file)
    open(time_file, 'a').\
         writelines(str(float(time.time()))+'\n')

# 根据不同发行版操作系统修改脚本开机自动执行配置。
if os.path.exists(auto_exec):
    pass
else:
    os.system('touch '+autoexec)

# 在预设的测试时长内保持测试继续执行并记录每次测试信息；
# 并在达到预设测试时长后停止测试并生成报告。
if TestCase().timer(time_file, duration):
    TestCase().time_record(time_file)
    TestCase().test_record(results_dir, boot_log, nic_list)
    if test_script in open(auto_exec, 'r').read():
        pass
    else:
        os.system('echo '+test_script+' >> '+ auto_exec )
        os.system('chmod +x '+ auto_exec)
    time.sleep(180)
    os.system('reboot')
else:
    tmp = open(auto_exec, 'r').readlines()
    del tmp[-1]
    open(auto_exec, 'w').writelines(tmp)
    TestCase().test_report(results_dir, time_file, nic_list, test_report)
