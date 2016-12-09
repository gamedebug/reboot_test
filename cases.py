import os, time, filecmp


class TestCase:


    def timer(self, time_file, duration):

        time_list = []
        test_duration = float(duration)

        for line in open(time_file):
            time_list.append(line)

        return float(time_list[-1])-float(time_list[0]) < test_duration*3600

    def counter(self, time_file):

        return int(os.popen('cat '+time_file+'| wc -l').read())

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
                os.system('dmesg > '+results_dir+'/'+str(info_folder)+'/'+boot_log)
                os.system('lspci | grep Ethernet > '+results_dir+'/'+\
                          str(info_folder)+'/'+nic_list)
                break

    def test_report():

        #counter = int(os.popen('cat '+time_file+'| wc -l').read())
        pass
    
