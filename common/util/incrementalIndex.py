#!/usr/bin/env python
# -*- coding:utf-8 -*-
from whoosh.filedb.filestore import FileStorage
from whoosh import index
from whoosh.index import FileIndex
from whoosh.fields import Schema, ID, TEXT
from whoosh.writing import AsyncWriter
import pymysql
from decimal import Decimal

def my_add_document(mykeys, row, writer):
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
    if mykeys == 1:
        mykeys = projKey
    elif mykeys == 2:
        mykeys = quesKey
    elif mykeys == 3:
        mykeys = varKey

    for key in mykeys:
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
    eval(docline)


def incremental_index(indexdir, indexname):
    storage = FileStorage(indexdir)
    ix = FileIndex(storage, indexname=indexname)
    writer = AsyncWriter(ix)
    return writer


def myCommit(writer):
    writer.commit()


if __name__ == '__main__':
    indexname = "metaproject"
    indexdir = "indexdir"
    mykeys = 1
    row = {}
    writer= incremental_index(indexdir, indexname)
    my_add_document(mykeys, row, writer)
    myCommit(writer)
