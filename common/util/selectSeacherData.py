#!/usr/bin/env python
# -*- coding:utf-8 -*-


from whoosh.filedb.filestore import FileStorage
from whoosh.index import exists_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from common.base import Config
from models.ProjectModel import SelectDataTablesInfo

def selectApp(clientContent, quesID=False, indexflag=2):
    myIndexDirFilePath = Config().get_content("indexFilePath")["filepath"]
    my_add_indexdir = myIndexDirFilePath + "/" + "indexdir"
    indexdir = my_add_indexdir
    storage = FileStorage(indexdir)

    fname = storage.list()
    indices = []

    indList = ["metaproject", "metaquestionnaire", "metavariable"]
    for ind in indList:
        indices.append(open_dir(indexdir, ind))

    ret = search(indices, indexflag, clientContent, quesID)
    return ret


def search(indices, indexflag, clientContent, quesID):
    inpval = indexflag
    qparsers = []
    if inpval == 1:
        categories = []
        for ix in indices:
            cat = list(ix.schema._fields.keys())
            for val in cat:
                if val in categories:
                    val = val + " - " + ix.indexname
                categories.append(val)

        for i in range(0, len(indices)):
            # qparsers.append(QueryParser(categories[inpval], indices[i].schema))
            qparsers.append(QueryParser("VarLebel", indices[i].schema))
    else:

        categories = []
        for ix in indices:
            categories.extend(list(ix.schema._fields.keys()))
            qparsers.append(MultifieldParser(categories,
                                             ix.schema))
    inp = clientContent

    data = inp.split('<==>')
    queries = [qparsers[i].parse(data[0].strip()) for i in range(0, len(qparsers))]

    if len(data) > 1:
        limits = int(data[1].strip())
        limits = 10

    results = []
    stats = {}

    for i in range(0, len(indices)):
        searcher = indices[i].searcher()
        res = searcher.search(queries[i], limit=10)
        if len(res) != 0:
            stats[indices[i].indexname] = len(res)
        else:
            continue
        results.extend(res)

    my_result = []
    projList = []
    quesList = []
    varList = []
    subVarList = []
    for i in results:
        i = dict(i)
        if "ProjectStatus" in i:
            if i["ProjectStatus"] == "1" and i["ProjectPublic"] == "2":
                projList.append(i)
        if "QuesStatus" in i:
            if i["QuesStatus"] == "1":
                quesList.append(i)
        if "VariableID" in i:
            if i["VarStatus"] == "1":
                varList.append(i)
                if quesID:
                    meta_data_tables = SelectDataTablesInfo(quesID)
                    if len(meta_data_tables) == 1:
                        DataTableID = meta_data_tables[0]["DataTableID"]
                        if DataTableID in i:
                            subVarList.append(i)

    my_result = [projList, quesList, varList, subVarList]
    # print(my_result)
    return my_result




if __name__ == '__main__':
    # indexflag = 2 # 1是分类索引2是全局索引
    clientContent = "教育"
    quesID = ""
    # selectApp(clientContent, quesID=quesID)
    res  = selectApp(clientContent)
    # print(res)
