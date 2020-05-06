import pymysql

config = {
    'host'     : 'localhost',
    'db'       : 'facedb',
    'user'     : 'face',
    'password' : 'face1234',
    'charset'  : 'utf8'
}

class db:
    def __init__(self):
        self.con = pymysql.connect(
            host=config['host'], 
            user=config['user'], 
            password=config['password'],
            db=config['db'],
            charset=config['charset']
        )
        self.cur = self.con.cursor(pymysql.cursors.DictCursor)

    def query(self, sql, s = None):
        try:
            if s is None:
                affect = self.cur.execute(sql)
            else :
                affect = self.cur.execute(sql,s)
            
            result = self.cur.fetchall()
            self.con.commit()
            return result,affect
        except BrokenPipeError:
            try:
                self.con.commit()
                self.con.close()
            except:
                pass
            self.con = pymysql.connect(
                host=config['host'], 
                user=config['user'], 
                password=config['password'],
                db=config['db'],
                charset=config['charset']
            )
            self.cur = self.con.cursor(pymysql.cursors.DictCursor)
            if s is None:
                affect = self.cur.execute(sql)
            else :
                affect = self.cur.execute(sql,s)
            
            result = self.cur.fetchall()
            self.con.commit()
            return result,affect
        except:
            try:
                self.con.commit()
                self.con.close()
            except:
                pass
            self.con = pymysql.connect(
                host=config['host'], 
                user=config['user'], 
                password=config['password'],
                db=config['db'],
                charset=config['charset']
            )
            self.cur = self.con.cursor(pymysql.cursors.DictCursor)
            if s is None:
                affect = self.cur.execute(sql)
            else :
                affect = self.cur.execute(sql,s)
            
            result = self.cur.fetchall()
            self.con.commit()
            return result,affect

    def release(self):
        self.con.commit()
        self.con.close()
