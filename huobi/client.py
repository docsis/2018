#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy
import sys
import time
import datetime
import rpyc
from rpyc.lib.compat import pickle

# 5370
class Log(object):
    ''' close ??'''
    def __init__(self, name="log.txt"):
        self.logfile = open(name, "ab")

    def write(self, s):
        TIMEFORMAT = '%Y-%m-%d_%H:%M:%S '
        self.logfile.write("\n" + datetime.datetime.now().strftime(TIMEFORMAT))
        self.logfile.write(s);
        self.logfile.flush();

    def close(self):
        self.write("CLOSE\n")
        self.logfile.close();

class Trade(object):

    def __init__(self):

        with open("/home/yajwu/kkey", "r") as f:
            HOSTIP, ACCESS_KEY, SECRET_KEY, accid = f.readlines()

        self.accid = int(accid)
        ACCESS_KEY = ACCESS_KEY.strip()
        SECRET_KEY = SECRET_KEY.strip()
        self.c = rpyc.connect(HOSTIP, 18861)
        self.c.root.setkey(ACCESS_KEY, SECRET_KEY)
        self.logger = Log()
        self.logger.write("START")
        self.update_data()

    def update_data(self):
        d = self.c.root.get_trade("btcusdt")
        self.btc_price = float(d['tick']['data'][0]['price'])

        d = self.c.root.get_balance(self.accid)
        btctrade = d['data']['list'][0]['balance']
        btcfrozen = d['data']['list'][1]['balance']
        usdttrade = d['data']['list'][2]['balance']
        usdtfrozen = d['data']['list'][3]['balance']
        self.btc_cnt = float(btctrade) + float(btcfrozen)
        self.btc_cnt = self.btc_cnt * self.btc_price
        self.usdt_cnt = float(usdttrade) + float(usdtfrozen)
        a,b,c,d,e = self.get_balance()
        self.logger.write("BALANCE %4.2f %4.2f $%4.2f $%4.2f" % (a,b,d,e))


    def get_balance(self):
        t = self.usdt_cnt + self.btc_cnt
        return self.btc_cnt, self.usdt_cnt, t, t*6.5, self.btc_price

    def orderlist_submitted(self):
        d = self.c.root.orders_list("btcusdt", "submitted")
        if d['status'] == "ok":
            self.submit_orders = d["data"]

    def orderlist_filled(self):
        d = self.c.root.orders_list("btcusdt", "filled")
        if d['status'] == "ok":
            self.filled_orders = d["data"]

    def save_kline(self):
        timestr = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        d = self.c.root.get_kline("btcusdt", '5min', 2000)
        if d['status'] == "ok":
            with open(timestr+"_5min.pickle",'wb') as f1:
                pickle.dump(d['data'],f1)

    def buy_order_limit(self, amount, price):
        # btc amount
        d = self.c.root.send_order(amount, "", "btcusdt", "buy-limit", price)
        print d

    def __del__(self):
        self.logger.close()



if __name__ == "__main__":
    trade = Trade()
    trade.save_kline()
    trade.update_data()

    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        while True:
            time.sleep(30)
            trade.update_data()

