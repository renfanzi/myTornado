#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, sys


filename = '/opt/code/my_code/myTornado/111.txt'

if not os.path.exists(filename):
    os.makedirs(filename)