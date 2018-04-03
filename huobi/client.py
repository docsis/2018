#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
import time
import rpyc
from rpyc.lib.compat import pickle


with open("/home/yajwu/kkey", "r") as f:
    HOSTIP, ACCESS_KEY, SECRET_KEY = f.readlines()

c = rpyc.connect(HOSTIP, 18861)

def print_orderlist():
    d = c.root.setkey(ACCESS_KEY, SECRET_KEY)
    d = c.root.orders_list("btcusdt", "filled")
    print d

def save_kline():
    d = c.root.get_kline("btcusdt", '15min', 2000)
    if d['status'] == "ok":
        f1 = open('kline.txt','wb')
        pickle.dump(d['data'],f1)
        f1.flush()
        f1.close()

save_kline()


