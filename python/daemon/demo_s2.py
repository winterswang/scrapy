from daemon import Daemon
import subprocess
import sys
import os
import time
import atexit
from signal import SIGTERM
from curl import Curl

class MyDaemon(Daemon):
    def run(self):
        f = open("/tmp/daemon-log","w")
        while True:
            if not self.check_scrapyd():
                f.write('starting the scrapyd')
                self.start_scrapyd()

#            if not self.check_projects('soufun_agent'):
#                res = self.add_project('soufun_agent')
#                f.write('%s' % res)
#
            res = self.check_spiders('soufun_agent')
            if res:
                f.write('%s' % res)
            else:
                f.write('starting the soufun_agent_spider\n')
                self.schedule_spiders('soufun_s2','soufun_agent')
            f.flush()
            time.sleep(10)

    #check the scrapyd is working on
    def check_scrapyd(self):
        pro = subprocess.Popen(['ps aux|grep scrapyd |grep -v grep'], stdout=subprocess.PIPE, shell=True)
        res = pro.communicate()[0]
        if res:
            return res
        else:
            return False

    #check the spiders is in the project or not
    def check_spiders(self,spider_name):

        pro = subprocess.Popen(['ps aux|grep %s |grep -v grep' %spider_name ],shell=True,stdout=subprocess.PIPE)
        res = pro.communicate()[0]
        if res:
            return res
        else:
            return False

    #check the project is in the scrapyd or not 
    def check_projects(self,projects):

        url = 'curl http://localhost:6800/listprojects.json'
        curl = Curl(url)
        res = curl.get()
        rlt = json.loads(res)
        for r in rlt['projects']:
            if r == 'soufun_s2':
                return True
        return False

    #start the scrapd server 
    def start_scrapyd(self):
        pro = subprocess.Popen(['cd /home/stephen/scrapy/; scrapyd &'], shell=True)

    #deploy the project and add into the scrapyd
    def add_project(self,project_name):

        pro = subprocess.Popen(['scrapyd-deploy soufun_s2 -p soufun_s2'],shell = True, stdout=subprocess.PIPE)
        res = pro.communicate()
        return res

    #schedule the spider to work
    def schedule_spiders(self,project_name,spider_name):
        
        url = 'http://localhost:6800/schedule.json'
        curl = Curl(url)
        dic = {'project':project_name,'spider':spider_name}
        res = curl.post(dic)
        rlt = json.loads(res)
        if rlt['status'] == 'ok':
            return True
        else:
            return False
        

if __name__ == "__main__":
    daemon = MyDaemon("/var/run/demodaemon.pid")
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)

