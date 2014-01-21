import MySQLdb
 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='ikuaizu@jia205',db='house',port=3306)
    cur=conn.cursor()
    agent_open_ids = ['oMJ6NjhtthUTIB2pypzH31abFaSE']
    #0 bruce 1 david 2 alan 3james
    #agent_open_ids = ['oMJNjqFk77K_S8TrHuyuzc2CdM4','oMJ6NjroCJknxIVI_x_YZJM31CZA','oMJ6Njjt2Uw3ze7oAGuVmR8hkkjo','oMJ6NjgAtZYvvRveMFpt_xY7tey4']
    for agent_open_id in agent_open_ids:
        print agent_open_id
        cur.execute('delete from user_vsf_wx where open_id =%s',agent_open_id)
        cur.execute('delete from agent_wx where open_id =%s',agent_open_id)
        cur.execute('delete from agent_store where agent_open_id =%s',agent_open_id)
        cur.execute('delete from house_soufun where agent_open_id = %s',agent_open_id)
        cur.execute('delete from soufun_house_desc where agent_open_id =%s',agent_open_id)
        for i in range(10):
            table = 'soufun_house_photo_'+str(i)
            cur.execute("delete from "+table+" where agent_open_id=%s",agent_open_id)

        print "clear the data successfull agent_open_id:"+agent_open_id
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
