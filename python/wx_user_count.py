# encoding: utf-8
import subprocess
import time
from datetime import date
from mysql_tools import MysqlTools

now = int(time.time())
oneday = now -86400

order = "cat /data/wwwlogs/wx_agent.log |awk -F '><' '{print$6,$8,$10}'|awk -F 'CreateTime' '{print $1,$2,$3}'|awk -F '[' '{print $3,$4,$5}'|awk -F ']]' '{print $1,$2}'|awk -F '>' '{print $1,$2}'|awk -F '</' '{print $1,$2}'|awk -F '! CDATA' '{print $1,$2}'|awk -F ' ' '{print $1,$2,$3}'"

order = order+" |awk '$2>%s' |sort |uniq -c -w 30|awk '{print $1,$2}'" % oneday
print order

result = []
pro = subprocess.Popen([order], shell=True,stdout=subprocess.PIPE)
res = pro.communicate()[0]

today =  date.today()
f = open("result/wx-"+str(today)+".txt","w")

if res:
   strlist = res.split("\n")
   for str in strlist:
       if len(str) > 10:
           strl = str.split(' ')
           sql = "select nickname from user_vsf_wx where open_id ='%s'" % strl[1]
           db = MysqlTools('127.0.0.1','root','ikuaizu@jia205','house',3306)
           ress1 = db.query(sql)

           db = MysqlTools('127.0.0.1','root','ikuaizu@jia205','house',3306)
           sql = "select agent_tel from agent_wx where open_id ='%s'" % strl[1]
           ress2 = db.query(sql)

           nickname = ''
           if ress1 and ress1[0]:
               nickname = ress1[0][0]

           type ='visitor'
           if ress2 and ress2[0]:
               type = 'agent'
           data = {'count':strl[0],'nickname':nickname,'open_id':strl[1],'type':type}
           result.append(data)

for res in result:
    prf =  "count: "+res['count']+"  open_id: "+res['open_id']+"  nickname: "+res['nickname']+" type: "+res['type']
    f.write(prf+"\n")

f.flush()
print today
