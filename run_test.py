#!/usr/bin/env python

from cases import TestCase
import os
import sys
import time
import json

current_dir = sys.path[0]
rec = json.load(open(current_dir+'/etc/config.json'))
results_dir = current_dir+str(rec['results'])
time_file = results_dir+str(rec['time_list'])
boot_log = str(rec['boot_log'])
nic_list = str(rec['nic_list'])
test_script = current_dir+str(rec['test_script'])
duration = str(float(rec['duration']))
auto_exec = str(rec['auto_exec'])

if os.path.exists(time_file):
    pass
else:
    TestCase().test_init(results_dir, time_file)
    open(time_file, 'a').\
         writelines(str(float(time.time()))+'\n')


if TestCase().timer(time_file, duration):
    TestCase().time_record(time_file)
    TestCase().test_record(results_dir, boot_log, nic_list)
    time.sleep(30)
    if test_script in open('/etc/rc.local', 'r').read():
        pass
    else:
        os.system('echo '+test_script+' >> '+ auto_exec )
        os.system('chmod +x '+ auto_exec)
    os.system('reboot')
else:
    tmp = open(auto_exec, 'r').readlines()
    del tmp[-1]
    open(auto_exec, 'w').writelines(tmp)
    TestCase().test_report()
