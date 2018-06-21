#-*-coding:utf-8-*-
import sqlite3
import cloud_reader

###------------have not finish ---------###

class Databaselite():
    def __init__(self):
        self.database_path = r'F:\code practice\triangle_restruct\tri.db'

    def query_all_table(self):  ## 查询数据库中所有表
        sql = '''select name from sqlite_master where type='table' order by name'''
        #sql = '''select * from sqlite_master'''   #所有表内容

        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        #print res
        return res

    def is_table_exist(self, table_name): ##查询表是否存在
        sql = '''select count(*) from sqlite_master where type='table' and name='%s' ''' % table_name
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        print table_name, res
        return res[0]

    def create_project_table(self):  ##创建项目表
        sql = '''create table project_table(
               pro_name CHAR[80],
               point_num INT, 
               pro_id INT
              )'''

        if not self.is_table_exist('project_table'):
            cx = sqlite3.connect(self.database_path)
            cur = cx.cursor()
            cur.execute(sql)
            cur.close()

            print 'project table create'
            return 1
        else:
            print 'project table already exist'
            return 0

    def query_project_by_name(self, project_name):  ##查询项目是否存在
        sql = '''select * from project_table where pro_name='%s' ''' % project_name
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        print project_name, res
        return res

    def query_project_by_id(self, pro_id):
        sql = '''select * from project_table where pro_id=%d ''' % pro_id
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        print pro_id, res
        return res

    def insert_project(self, pro_name, pro_num, pro_id):  ##插入项目
        sql = '''insert into project_table (pro_name, point_num, pro_id) values('%s', %d, %d)''' % (pro_name, pro_num, pro_id)
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        cx.commit()
        cur.close()
        print 'insert successful'

    def remove_project(self, pro_id):
        sql = '''delete from project_table where pro_id=%d ''' % pro_id
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        cx.commit()
        cur.close()
        print 'delete successful'

    def update_project_info(self):
        pass

    def create_pro_data_table(self, table_name):
        sql = '''create table '%s'(
                       x INT ,
                       y INT,  
                       z INT
                      )''' % table_name

        if not self.is_table_exist(table_name):
            cx = sqlite3.connect(self.database_path)
            cur = cx.cursor()
            cur.execute(sql)
            cur.close()
            print 'project table create'
        else:
            print 'project table already exist'

    def insert_data(self, table_name, p_list):
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        for x, y, z in p_list:
            sql = '''insert into '%s' (x, y, z) VALUES (%d, %d, %d)''' % (table_name, x, y, z)
            cur.execute(sql)
        cx.commit()
        cur.close()

    def remove_table(self, table_name):
        sql = '''drop table %s''' % table_name
        cx = sqlite3.connect(self.database_path)
        cur = cx.cursor()
        cur.execute(sql)
        cur.close()


class DatabaseHandle():
    def __init__(self, database=Databaselite()):
        self.database = database

    def query_all_table(self):
        return self.database.query_all_table()

    def is_table_exist(self, table_name):
        return self.database.is_table_exist(table_name)

    def create_project_table(self):
        return self.database.create_project_table()

    def query_project_by_name(self, project_name):
        return self.database.query_project_by_name(project_name)

    def query_project_by_id(self, project_id):
        return self.database.query_project_by_id(project_id)

    def insert_project(self, pro_name, pro_num, pro_id):
        return self.database.insert_project(pro_name, pro_num, pro_id)

    def remove_project(self, pro_id):
        return self.database.remove_project(pro_id)

    def create_pro_data_table(self, table_name):
        return self.database.create_pro_data_table(table_name)

    def insert_data(self, table_name, p_list):
        return self.database.insert_data(table_name, p_list)

    def remove_table(self, table_name):
        return self.database.remove_table(table_name)


def test_database():
    db_manage = Databaselite()
    db_manage.create_project_table()
    db_manage.query_all_table()
    # db_manage.remove_table('project_table')
    # db_manage.query_all_table()
    db_manage.query_project_by_name('123')
    #
    db_manage.insert_project('zpc', 200, 1234567)
    db_manage.query_project_by_name('zpc')
    db_manage.query_project_by_id(1234567)
    db_manage.query_project_by_id(12)

    db_manage.remove_project(1234567)
    db_manage.query_project_by_name('zpc')
    db_manage.query_project_by_id(1234567)

    print
    db_manage.create_pro_data_table('test_data')
    db_manage.insert_data('test_data', 100, 100, 100)


if __name__ == '__main__':
    test_database()
