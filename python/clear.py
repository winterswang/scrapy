import MySQLdb
 
try:
    conn=MySQLdb.connect(host='192.168.1.99',user='root',passwd='ikuaizu@205',db='house',port=3306)
    cur=conn.cursor()
    agent_open_id = 'oMJ6NjqFk77K_S8TrHuyuzc2CdM4'
    cur.execute('delete from agent_store where agent_open_id =%s',agent_open_id)
    cur.execute('delete from house_soufun where agent_open_id = %s',agent_open_id)
    cur.execute('delete from soufun_house_desc where agent_open_id =%s',agent_open_id)
    for i in range(10):
        table = 'soufun_house_photo_'+str(i)
        cur.execute("delete from "+table+" where agent_open_id=%s",agent_open_id)
    cur.close()
    conn.close()
    print "clear the data successfull agent_open_id:"+agent_open_id
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
