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
            res = self.check_spiders('soufun_agent')
            if res:
                f.write('%s' % res)
            else:
                f.write('starting the soufun_agent_spider\n')
                url = 'http://localhost:6800/schedule.json'
                curl =Curl(url)
                dic = {'project':'soufun_s2','spider':'soufun_agent'}
                res = curl.post(dic) 
            f.flush()
            time.sleep(10)

    def check_spiders(self,spider_name):

            pro = subprocess.Popen(['ps aux|grep %s |grep -v grep' %spider_name ],shell=True,stdout=subprocess.PIPE)
            res = pro.communicate()[0]
            if res:
                return res
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

