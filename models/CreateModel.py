#!/usr/bin/env python
# -*- coding:utf-8 -*-

# !/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from decimal import Decimal
from common.base import MyPymysql, MyGuid, my_datetime, my_log


def CreateMetaProj(data):

    sql = "insert into `meta_project` SET ProjectID={}, UserID={}, ProjectName='{}', ProjectOrgan='{}', ProjectSubject='{}', " \
          "SubjectField={}, ProjectLevel={}, ProjectSource={}, FundsSource={}, ProjectSummary='{}', CycleType={}, CycleSpan='{}', " \
          "TeamIntroduction='{}', ProjectPublic={}, ProjectStatus={}, EditUserID={};".format(
        data["ProjectID"],
        data["UserID"],
        data["ProjectName"],
        data["ProjectOrgan"],
        data["ProjectSubject"],
        data["SubjectField"],
        data["ProjectLevel"],
        data["ProjectSource"],
        data["FundsSource"],
        data["ProjectSummary"],
        data["CycleType"],
        int(data["CycleSpan"]),
        data["TeamIntroduction"],
        data["ProjectPublic"],
        data["ProjectStatus"],
        data["EditUserID"])
    # print(sql)
    ret = MyPymysql('metadata')
    ret.idu_sql(sql)
    ret.close()



