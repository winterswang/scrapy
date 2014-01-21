import MySQLdb
 
try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='ikuaizu@jia205',db='house',port=3306)
    cur=conn.cursor()
    cur.execute('select * from agent_store')
    result = cur.fetchall()
    for res in result:
       print res
    cur.close()
    conn.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
