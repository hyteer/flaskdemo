# encoding:utf-8
import pymysql,time
'''
db_cfg = {
    'host': '192.168.198.128',
    'user': 'tester',
    'passwd': '111',
    'db': 'temptest'
}
'''

class Mysql():
    cfg = {
    'host': '',
    'user': '',
    'passwd': '',
    'db': ''
}
    conn = None
    cur = None

    def connDB(self):   #连接数据库函数     
        self.conn = pymysql.connect(host=self.cfg['host'],user=self.cfg['user'],passwd=self.cfg['passwd'],
                             db=self.cfg['db'],charset='utf8')
        self.cur=self.conn.cursor()
        return (self.conn,self.cur)

    def exeUpdate(self,cur,sql): #更新语句，可执行update,insert语句
        sta=cur.execute(sql)
        return(sta)

    def exeDelete(self,cur,*IDs): #删除语句，可批量删除 
        for eachID in IDs:
            sta=cur.execute('delete from users where id=%d'% int(eachID))
            return (sta)

    def exeQuery(self,cur,sql):  #查询语句 
        cur.execute(sql)
        return (cur)

    def executeSQL(self,cur,sql=""):
        try:
            self.conn.ping()
        except Exception,e:
            print("Msql出了问题")
            print(str(e))
            while True:
                try:
                    self.conn = pymysql.connect(host=self.cfg['host'],user=self.cfg['user'],passwd=self.cfg['passwd'],
                             db=self.cfg['db'],connect_timeout=60,charset='utf8')
                    break
                except Exception,e:
                    print("尝试重连接失败")
                    time.sleep(2)
                    continue
            self.cur=Mysql.conn.cursor()
        try:
            self.cur.execute(sql)
            self.conn.commit()
            return 1
        except Exception,e:
            print(str(e))
            return 0

    def connClose(self):    #关闭所有连接 
        self.cur.close()
        self.conn.close()

    def init_db(self):
        self.connDB()

    #@staticmethod
    def init_app(self,app):
        """
        Initializes mysql settings from the application config.
        We can set up mysql db instance at configration time.
        :param app: etc. Flask Application instance
        :return: state
        """

        cfg = app.config.get('MYSQL_CONFIG')
        self.cfg['host'] = cfg['host']
        self.cfg['user'] = cfg['user']
        self.cfg['passwd'] = cfg['passwd']
        self.cfg['db'] = cfg['db']
        print "init mysql config with success..."

        state = self.init_db()
        print "mysql connection has been made..."

        return state



