import pymysql
from typing import Dict
from singleton import singleton
from threading import Lock

LK = Lock()

data_base_config = {
    'host': '192.168.188.231',
    'user': 'root',
    'password': 'u4bVDgdvELq6Nmhb',
    'port': 33061
}


class DB:
    def __init__(self, db_name):
        # self.db = pymysql.connect(db=db_name,cursorclass=pymysql.cursors.DictCursor,**data_base_config).cursor()   # type: pymysql.cursors.Cursor
        self.db = pymysql.connect(db=db_name, cursorclass=pymysql.cursors.DictCursor, **data_base_config)
        self.cur = self.db.cursor()

    def query_one(self, sql):
        with LK:
            self.cur.execute(sql)
            res = self.cur.fetchone()
        return res

    def query_all(self, sql):
        with LK:
            self.cur.execute(sql)
            res = self.cur.fetchall()
        return res

    def execute_one(self, sql):
        with LK:
            self.cur.execute(sql)
            res = self.db.commit()
        return res

    def __del__(self):
        self.cur.close()
        self.db.close()
        del self.db


@singleton.Singleton
class DbManager:
    def __init__(self):
        self.dbs: Dict[str, DB] = {}

    def add_db(self, db_name):
        assert db_name not in self.dbs
        self.dbs[db_name] = DB(db_name)

    def remove_db(self, db_name):
        del self.dbs[db_name]

    def query_one(self, db_name, sql):
        return self.dbs[db_name].query_one(sql)

    def query_all(self, db_name, sql):
        return self.dbs[db_name].query_all(sql)

    def execute_one(self, db_name, sql):
        return self.dbs[db_name].execute_one(sql)

    def __del__(self):
        for db in self.dbs:
            del db


def check_db_connect(db_name):
    if db_name not in DBM.dbs:
        DBM.add_db(db_name)


DBM = DbManager.instance()  # type: DbManager
# DBM = DbManager()      # type: DbManager

if __name__ == '__main__':
    conn = pymysql.connect(db='new-himo-micro-preferential', cursorclass=pymysql.cursors.DictCursor, **data_base_config)
    cur = conn.cursor()
    cur.execute("select SUM(balance) from user_gift_cards where status = 'used'"
                "and stop_usage > now() and user_id = {} and "
                "(give_status is null or give_status != 'giving') and "
                "deleted_at is null".format('4657733'))
    a = cur.fetchone()
    print(a)
