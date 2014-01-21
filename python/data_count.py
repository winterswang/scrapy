from datetime import *
import time
import MySQLdb

#user data about total agent count,everyday new add agent count every city agent count
data = {'totalCount':0,'newAddCount':0,'cityCount':[]}

#house data about total house publish count, total house syn count and every user hpc and hsc 
house_data = {'totalHPCount':0,'newHPCount':0,'totalHSCount':0,'newHSCount':0,'userCount':[]}

today = date.today()
f = open("result/"+str(today)+".txt","w") 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='ikuaizu@jia205',db='house',port=3306)
    cur=conn.cursor()
    cur.execute('select count(*) from agent_wx')

    result = cur.fetchone()
    data['totalCount'] = result[0]

    cur.execute("select count(*) from agent_wx where create_time like '"+str(date.today())+"%'")
    result = cur.fetchone()
    data['newAddCount'] = result[0]    

    cur.execute('select count(*),status from house_soufun group by status')
    result = cur.fetchall()
    for res in result:
        if res[1] == 1:
            house_data['totalHPCount'] = res[0]
        if res[1] == 0:
            house_data['totalHSCount'] = res[0] 
    cur.execute('select count(*),status from house_soufun where createtime =%s group by status',int(time.time()))
    result = cur.fetchall()
    for res in result:
        if res[1] == 1:
            house_data['newHPCount'] = res[0]
        if res[1] == 0:
            house_data['newHSCount'] = res[0]

    cur.execute('select agent_open_id, count(agent_open_id) from house_publish group by agent_open_id')
    result = cur.fetchall()
    for res in result:
        dic = {'agent_open_id':res[0],'housePublishCount':res[1]}
        house_data['userCount'].append(dic)

    cur.execute('select open_id,count(city),city from user_vsf_wx where open_id in (select open_id from agent_wx) group by city')
    result = cur.fetchall()
    for res in result:
        dic = {'agent_open_id':res[0],'agentCount':res[1],'city':res[2]}
        data['cityCount'].append(dic)

    cur.close()
    conn.close()

    print date.today()
    print int(time.time())
    res = 'totalCount:'+str(data['totalCount'])+"\n"
    res = res+'newAddCount:'+str(data['newAddCount'])+"\n"

    for d in data['cityCount']:
        res =res+str(d)+"\n"
    f.write(res)
    f.write("############################################################################\n")
    res1 = 'totalHPCount:'+str(house_data['totalHPCount'])+"\n"
    res1 = res1+'newHPCount:'+str(house_data['newHPCount'])+"\n"

    res1 = res1 + 'totalHSCount:'+str(house_data['totalHSCount'])+"\n"
    res1 = res1 + 'newHSCount:' +str(house_data['newHSCount'])+"\n"
         
    for hd in house_data['userCount']:
        res1 = res1 + str(hd)+"\n"
    f.write(res1)
    f.flush()

except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
