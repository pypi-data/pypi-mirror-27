# -*- coding:utf-8 -*-
"""zhao.xin_mysql
"""

import MySQLdb

DEFAULT_ENGIN = 'InnoDB'
DEFAULT_CHARSET = 'utf8'


def show_database_error(error):
    """输出MySQL错误信息"""
    try:
        number = error.args[0]
        message = error.args[1]
        print(f'MySQL Error[{number}]: {message}')
    except IndexError:
        print(f'MySQL Error: {error}')


class MySQL(object):
    """MySQL类"""

    def __init__(self, **kwargs):
        self.connection = None
        try:
            self.schema = kwargs.get('db')
            kwargs['connect_timeout'] = kwargs.get('connect_timeout') or 5
            kwargs['charset'] = kwargs.get('charset') or 'utf8'  # utf8 default
            self.connection = MySQLdb.connect(**kwargs)
        except self.connection.Error as error:
            show_database_error(error)
            raise error

    def __del__(self):
        # print('MySQL DATABASE CONNECTION CLOSED.')
        if self.connection.open:
            self.connection.close()

    def query_one(self, sql):
        """查询单行数据"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
        except self.connection.Error as error:
            show_database_error(error)
            raise error

    def query(self, sql):
        """查询多行数据"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor
        except self.connection.Error as error:
            show_database_error(error)
            raise error

    @property
    def version(self):
        """服务器MySQL版本"""
        return self.query_one("SELECT VERSION();")[0]

    @property
    def table_names(self):
        """获取数据表表名列表"""
        return self.query_one("SHOW TABLES;")

    def table_columns(self, table_name):
        """返回数据表字段信息"""
        sql = ("SELECT COLUMN_NAME, ORDINAL_POSITION, COLUMN_DEFAULT, IS_NULLABLE, "
               "COLUMN_TYPE, COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS "
               f"WHERE table_schema='{self.schema}' and table_name='{table_name}' "
               "and EXTRA != 'auto_increment' ORDER BY ORDINAL_POSITION;")
        return self.query(sql)

    def execute(self, sql):
        """执行修改数据库的语句"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('START TRANSACTION;')  # 必要吗？
                cursor.execute(sql)
                self.connection.commit()
                return cursor.rowcount
        except self.connection.Error as error:
            self.connection.rollback()
            show_database_error(error)
            raise error

    def create_table(self, name, columns,
                     engine=DEFAULT_ENGIN,
                     charset=DEFAULT_CHARSET):
        """创建数据表"""
        if not name in self.table_names:
            sql = (f"CREATE TABLE IF NOT EXISTS `{name}`({columns}) "
                   f"ENGINE='{engine}' DEFAULT CHARSET='{charset}';")
            self.execute(sql)
        return bool(name in self.table_names)

    def drop_table(self, name, comfirm):
        """删除数据表"""
        if comfirm != 'I_DO_KNOW_WHAT_I_AM_DOING!':
            raise ImportWarning('MySQL Warning: Droping table CASUALLY!!')
        elif name in self.table_names:
            self.execute(f"DROP TABLE `{name}`;")
        return bool(name not in self.table_names)
