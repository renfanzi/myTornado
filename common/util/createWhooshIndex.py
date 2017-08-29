#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import os
from whoosh.index import create_in
from jieba.analyse import ChineseAnalyzer
from decimal import Decimal
from whoosh.fields import Schema, TEXT
import configparser


analyzer = ChineseAnalyzer()


class Config(object):
    """
    # Config().get_content("user_information")
    """
    def __init__(self, config_filename="zk_css.cnf"):
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class base_pymysql(object):
    def __init__(self, host, port, user, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = pymysql.connect(host=self.db_host, port=self.db_port, user=self.user,
                                    passwd=self.password, db=self.db, charset="utf8")
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)


class MyPymysql(base_pymysql):
    """
    Basic Usage:
        ret = My_Pymysql('test1')
        res = ret.selectone_sql("select * from aaa")
        print(res)
        ret.close()
    Precautions:
        Config.__init__(self, config_filename="zk_css.cnf")
    """

    def __init__(self, conf_name):
        self.conf = Config().get_content(conf_name)
        # self.conf = {"host": "192.168.1.126", "port": 3306, "db_name": "db_metadata", "user": "root", "password": "123456"}
        super(MyPymysql, self).__init__(**self.conf)
        self.connect()

    def idu_sql(self, sql):
        # adu: insert, delete, update的简写
        # 考虑到多语句循环, try就不写在这里了
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_sql(self, sql, value=None):
        # adu: insert, delete, update的简写
        self.cursor.execute(sql, value)
        self.conn.commit()

    def selectone_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchone()

    def selectall_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
        self.conn = None
        self.cursor = None

def parse_db(tables, conn, indexname, schema, indexdir, keys):
    table = tables
    sql = "select * from %s;" % table
    rows = conn.selectall_sql(sql)
    conn.close()
    # keys = rows[0].keys()
    s = "Schema("
    for key in keys:
        s += key.replace('\n', '').replace('/r', '').replace('\t', '').replace(' ', '') + '=TEXT(stored=True, analyzer=analyzer), '
    s = s.rstrip(", ")
    s += ")"
    schema = eval(s)
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema=schema, indexname=indexname)
    writer = ix.writer()
    for row in rows:
        docline = """writer.add_document("""
        for key in keys:
            val = row[key]
            if not val:
                val = ""
            elif isinstance(val, (Decimal,)):
                val = str(val)

            else:
                val = pymysql.escape_string(str(val))
            docline += key + '="' + val + '", '
        docline = docline.rstrip(", ")
        docline += """)"""
        exec(docline)
    writer.commit()


def escape(s, obj="’"):
    ret = ''
    for x in s:
        if x == obj:
            ret += '\\'
        ret += x
    return ret


def app():

    tables = ["meta_project", "meta_questionnaire", "meta_variable"]
    filepath = Config().get_content("indexFilePath")["filepath"]
    # filepath = "/data/zk_css/"
    indexdir = "indexdir"
    filename = filepath + "/" + indexdir
    projKey = ["ProjectID", "UserID", "ProjectName", "ProjectOrgan", "ProjectSubject", "SubjectField", "ProjectLevel",
               "ProjectSource", "FundsSource", "ProjectSummary", "CycleType", "CycleSpan", "TeamIntroduction",
               "ProjectPublic", "ProjectStatus", "EditUserID", "EditTime", "CreateTime", "StartTime", "EndTime"]
    quesKey = ["QuesID", "ProjectID", "QuesDataForm", "QuesTitle", "QuesSummary", "QuesKeywords", "QuesObject",
               "QuesDataChannel", "SamplePlan", "ResponseSituation", "DataTeam", "QuesDataTown",
               "MinimumGeographicUnit",
               "DataCoverageTime", "QuesStartTime", "QuesEndTime", "WeightDescription", "CreateTime", "QuesStatus"]
    varKey = ["VariableID", "DataTableID", "OrderNum", "VarName", "VarType", "VarWidth", "VarDecimals", "OriginFormats",
              "VarMeasure", "VarValues", "VarMissing", "VarTopic", "VarLabel", "OriginQuestion", "OtherLangLabel",
              "DataFrom", "DeriveFrom", "VarRole", "VarVersion", "ReviseFrom", "ReviseTime", "ReviseUserID", "VarNote",
              "VarStatus"]
    docline = """writer.add_document("""

    for table in tables:
        if table == "meta_project":
            keys = projKey
        elif table == "meta_questionnaire":
            keys = quesKey
        elif table == "meta_variable":
            keys = varKey
        db_connect = MyPymysql("metadata")
        name = table.split("_")
        dbname = name[0] + name[1]
        parse_db(table, db_connect, indexname=dbname, schema="", indexdir=filename, keys=keys)


if __name__ == '__main__':
    # 这个文件我可以写个接口呀,哈哈哈真笨

    app()
