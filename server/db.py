from pymysql import connect
from config import *

class DB(object):

    def __init__(self):
        """初始化数据库连接"""

        # 创建数据库连接
        self.conn = connect(host=DB_HOST,
                            user = DB_USER,
                            password = DB_PASS,
                            database=DB_NAME,
                            port = DB_PORT)
        # 获得游标
        self.cursor = self.conn.cursor()

    def get_one(self,sql):
        """执行SQL查询"""

        # 执行SQL查询
        self.cursor.execute(sql)
        # 查询结果
        query_result = self.cursor.fetchone()

        if not query_result:
            return None
        # 获得字段列表
        fields = [field[0] for field in self.cursor.description]

        # 保存返回结果
        return_data = dict()
        for field,value in zip(fields,query_result):
            return_data[field] = value

        return return_data

    def close(self):
        '''关闭数据库连接'''

        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    db = DB()
    print(db.get_one("select * from users where user_name='emma'"))

