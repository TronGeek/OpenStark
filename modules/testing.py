from tornado import gen
from tornado.log import app_log as log
import tormysql
import time


class TestingModule(object):
    """
    动态连接数据库查询
    """
    def __init__(self, engine, host, user, password, database, sql, port=3306, filtering='', do='', charset='utf8'):
        self.engine = engine
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.sql = sql
        self.filter = filtering
        self.do = do

    # 建立数据库连接
    def _conn(self):
        if self.engine == 'mysql':
            conn = tormysql.helpers.ConnectionPool(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.database,
                charset=self.charset
            )
            self.pool = conn
        else:
            self.pool = None

    # 获取所有查询结果
    @gen.coroutine
    def get_all_result(self):
        result = []
        for i in range(3):
            self._conn()
            log.info('{}#查询SQL: {}'.format(i, self.sql))
            cursor = yield self.pool.execute(self.sql)
            result = cursor.fetchall()
            cursor.close()
            if result:
                break
            time.sleep(1)
        yield self.pool.close()
        return result

    # 获取查询结果的第一条
    @gen.coroutine
    def get_one_result(self):
        result = []
        for i in range(3):
            self._conn()
            log.info('{}#{} 查询SQL: {}'.format(i, self.host, self.sql))
            cursor = yield self.pool.execute(self.sql)
            result = cursor.fetchone()
            cursor.close()
            if result:
                break
            time.sleep(1)
        yield self.pool.close()
        return result
