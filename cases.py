import os
import time
import filecmp


class TestCase:

    def timer(self, time_file, duration):

        time_list = []
        test_duration = float(duration)

        for line in open(time_file):
            time_list.append(line)

        return float(time_list[-1])-float(time_list[0]) < test_duration*3600

    def test_init(self, results_dir, time_file):

        if os.path.exists(results_dir):
            pass
        else:
            os.system('mkdir '+results_dir)

        if os.path.exists(time_file):
            pass
        else:
            os.system('touch '+time_file)

    def time_record(self, time_file):

        open(time_file, 'a').\
            writelines(str(float(time.time()))+'\n')

    def test_record(self, results_dir, boot_log, nic_list):

        info_folder = 0

        while True:
            if os.path.exists(results_dir+'/'+str(info_folder)):
                info_folder += 1
            else:
                os.system('mkdir '+results_dir+'/'+str(info_folder))
                os.system('dmesg > '+results_dir+'/'+str(info_folder)+'/'+\
                          boot_log)
                os.system('lspci | grep Ethernet > '+results_dir+'/'+\
                          str(info_folder)+'/'+nic_list)
                break

    def test_report(self, results_dir, time_file, nic_list, report):

        counter = int(os.popen('cat '+time_file+'| wc -l').read())

        results_list=[]
        for num in os.listdir(results_dir):
            if num.isdigit():
                results_list.append(num)
            else:
                pass

        issue = []
        cmp_list=[]
        for num in results_list:
            cmp_list.append(filecmp.cmp(results_dir+'/0'+'/'+\
                            nic_list, results_dir+'/'+num+'/'+nic_list))
            if filecmp.cmp(results_list+'/0'+'/'+nic_list,\
                           results_list+'/'+num+'/'+nic_list):
                pass
            else:
                issue.append(num)

        if False in cmp_list:
            result = 'Failed'
        else:
            result = 'Passed'

        if os.path.exists(results_dir+'/'+report):
            os.system('rm -fr '+results_dir+'/'+report)
        else:
            pass

        os.system('touch '+results_dir+'/'+report)
        open(results_dir+'/'+report, 'a').write('Test result: '+result+'\n')
        open(results_dir+'/'+report, 'a').write('Reboot times: '+str(counter)+'\n')
        open(results_dir+'/'+report, 'a').write('Issue list: '+str(issue)+'\n')
