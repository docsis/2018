#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import pandas as pd
from comm import *

KLINE_TT_COLS = ['id', 'open', 'high', 'low', 'close', 'amount', 'count', 'vol']
csv_fname = "5min_kline1.csv"

def save_to_csv():
    d = read_pickle("./", "pickle")
    df = pd.DataFrame(d, columns=KLINE_TT_COLS)
    df['id'] = df['id'].apply(sec2date)
    df.to_csv(csv_fname)

save_to_csv()
df = pd.read_csv(csv_fname)

usdt_cnt = 200
btc_cnt = 0.03

HIGH = 170
LOW = 170

unit = 0.007

buy_orders = []
sell_orders = []

for idx in df.index:
    t,o,h,l = df.loc[idx].values[1:5]
    #print idx, t, o, h,l
    if len(buy_orders) == 0 or len(sell_orders) == 0:
        buy_orders.append(o-LOW)
        sell_orders.append(o+HIGH)
    else:
        if l < buy_orders[0]:
            btc_cnt += unit
            usdt_cnt -= unit * buy_orders[0]
            if usdt_cnt < 0:
                print "!!!! usdt_cnt", usdt_cnt
            print ">> buy", buy_orders[0], usdt_cnt, btc_cnt
            del(buy_orders[0])
        if h > sell_orders[0]:
            btc_cnt -= unit
            usdt_cnt += unit * sell_orders[0]
            if btc_cnt < 0:
                print "!!!! btc_cnt", btc_cnt
            print ">> sell",sell_orders[0], usdt_cnt, btc_cnt
            del(sell_orders[0])

    if len(buy_orders) == 0 or len(sell_orders) == 0:
        if len(buy_orders):
            del(buy_orders[0])
        if len(sell_orders):
            del(sell_orders[0])
        buy_orders.append(o-LOW)
        sell_orders.append(o+HIGH)

    if idx == 0:
        print "balance: ", o, usdt_cnt, btc_cnt, usdt_cnt + btc_cnt*o
print "balance: ", o, usdt_cnt, btc_cnt, usdt_cnt + btc_cnt*o
