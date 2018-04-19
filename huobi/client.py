#!/usr/bin/python
# -*- coding: utf-8 -*- import numpy
import sys
import time
import datetime
import rpyc
from cmd import Cmd
from comm import sec2date
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
        self.vbalance = {}

    def update_data(self):
        #d = self.c.root.get_trade("btcusdt")
        #self.btc_price = float(d['tick']['data'][0]['price'])

        d = self.c.root.get_balance(self.accid)
        for i in d['data']['list'][:12]:
            if i['balance'] != "0.000000000000000000":
                self.vbalance[i['currency']] = (i['type'], i['balance'])

    def get_balance(self):
        self.update_data()
        for k,v in self.vbalance.iteritems():
            print "%-4s %-6s %s" % (k, v[0], v[1])
        return

    def orderlist_submitted(self):
        d = self.c.root.orders_list("btcusdt", "submitted")
        if d['status'] == "ok":
            self.submit_orders = d["data"]
        return self.filled_orders

    def orderlist_filled(self):
        d = self.c.root.orders_list("btcusdt", "filled")
        if d['status'] == "ok":
            self.filled_orders = d["data"]
        return self.filled_orders

    def save_kline(self, mins="5min"):
        timestr = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        d = self.c.root.get_kline("btcusdt", mins, 2000)
        if d['status'] == "ok":
            with open(timestr+"_"+mins+".pickle",'wb') as f1:
                pickle.dump(d['data'],f1)

    def buy_order_limit(self, amount, price):
        # btc amount
        d = self.c.root.send_order(amount, "", "btcusdt", "buy-limit", price)

    def get_trade(self, symbol):
        return self.c.root.get_trade(symbol)

    def __del__(self):
        self.logger.close()

class MyCmd(Cmd):

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def preloop(self):
        self.trade = Trade()

    def do_balance(self, args):
        """ Acount balance """
        self.trade.get_balance()

    def do_order(self, args):
        """ Order list """
        f = self.trade.orderlist_filled()
        s = self.trade.orderlist_submitted()

        for i in f:
            print i['symbol'], sec2date(int(i['finished-at'])/1000), i['price'], i['amount']

        for i in s:
            print i['symbol'], sec2date(int(i['finished-at'])/1000), i['price'], i['amount']

    def do_trade(self, args):
        """ trade tick """
        if len(args) == 0:
            args = 'btcusdt'
        d = self.trade.get_trade(args);
        if d['status'] == 'ok':
            v = d['tick']['data']
            print v[0]['price']

if __name__ == "__main__":

    prompt = MyCmd()
    prompt.prompt = "> "
    prompt.cmdloop("==== start cmdloop =====")
