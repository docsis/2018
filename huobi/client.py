#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
import datetime
import rpyc
from rpyc.lib.compat import pickle


with open("/home/yajwu/kkey", "r") as f:
    HOSTIP, ACCESS_KEY, SECRET_KEY, accid = f.readlines()

accid = int(accid)
ACCESS_KEY = ACCESS_KEY.strip()
SECRET_KEY = SECRET_KEY.strip()

c = rpyc.connect(HOSTIP, 18861)
d = c.root.setkey(ACCESS_KEY, SECRET_KEY)

def print_orderlist_submitted():
    d = c.root.orders_list("btcusdt", "submitted")
    if d['status'] == "ok":
        orders = d["data"]
        for e in orders:
            print e

def print_orderlist_filled():
    d = c.root.orders_list("btcusdt", "filled")
    if d['status'] == "ok":
        orders = d["data"]
        for e in orders:
            print e

def save_kline():
    timestr = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
    d = c.root.get_kline("btcusdt", '5min', 2000)
    if d['status'] == "ok":
        with open(timestr+"_5min.pickle",'wb') as f1:
            pickle.dump(d['data'],f1)

def get_balance():
    global accid
    d = c.root.get_balance(accid)
    btc = d['data']['list'][0]
    print d['data']['list'][1]
    usdt = d['data']['list'][2]
    print d['data']['list'][3]
    print btc
    print usdt

def buy_order_limit(amount, price):
    d = c.root.send_order(amount, "", "btcusdt", "buy-limit", price)
    print d


#buy_order_limit("0.001", "5000")
#print_orderlist_submitted()
#print_orderlist_filled()
save_kline()
#get_balance()
