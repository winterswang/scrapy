import MySQLdb

class MysqlTools:

    def __init__(self,DB_HOST, DB_USER, DB_PASSWD, DB_NAME, DB_PORT):
        self.DB_HOST = DB_HOST
        self.DB_USER = DB_USER
        self.DB_PASSWD = DB_PASSWD
        self.DB_PORT = DB_PORT
        self.DB_NAME = DB_NAME

        self.conn = self.get_connection()

    def get_connection(self):
        return MySQLdb.connect(
                               host=self.DB_HOST, user=self.DB_USER, passwd=self.DB_PASSWD, db=self.DB_NAME, port=self.DB_PORT
                              )

    def query(self,sql):
        try:
            cur=self.conn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            self.conn.close()
            return result
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def update(self,sql):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            self.conn.commit()
            cur.close()
            self.conn.close()
            return True
        except MySQLdb.Error,e:
            print "MYsql Error %d: %s" % (e.args[0], e.args[1])

if __name__=="__main__":
    db = MysqlTools('127.0.0.1','root','ikuaizu@jia205','house',3306)
    print db.query('show tables;')
