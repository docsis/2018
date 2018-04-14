#!/usr/bin/python
# -*- coding: utf-8 -*-
from comm import *


df = read_pickle(".", "pickle")
save_to_csv(df)


def run(high, low, unit_b=0.002, unit_s=0.0055):
    init_p = 0
    init_u = 0
    init_b =0

    usdt_cnt = 200
    btc_cnt = 0.03

    HIGH = high
    LOW = low

    buy_orders = []
    sell_orders = []

    start = 1000 
    end =-1000 
    cnt = 0

    for idx in df.index[start:end]:
        try:
            t,o,h,l = df.loc[idx].values[0:4]
        except :
            print "!! unpack error ", idx, df.loc[idx].values[0:4]

        if idx == df.index[start]:
            init_p = o; init_u = usdt_cnt; init_b = btc_cnt 
            #print "balance: ", o, usdt_cnt, btc_cnt, usdt_cnt + btc_cnt*o

        if len(buy_orders) == 0 or len(sell_orders) == 0:
            buy_orders.append(o-LOW)
            sell_orders.append(o+HIGH)
        else:
            if l < buy_orders[0]:
                btc_cnt += unit_b
                usdt_cnt -= unit_b * buy_orders[0]
                if usdt_cnt < 0:
                    print "!!!! usdt_cnt", usdt_cnt
                #print ">> buy", buy_orders[0], usdt_cnt, btc_cnt
                cnt += 1
                del(buy_orders[0])
            if h > sell_orders[0]:
                btc_cnt -= unit_s
                usdt_cnt += unit_s * sell_orders[0]
                if btc_cnt < 0:
                    print "!!!! btc_cnt", btc_cnt
                #print ">> sell",sell_orders[0], usdt_cnt, btc_cnt
                del(sell_orders[0])
                cnt += 1

            if len(buy_orders) == 0 or len(sell_orders) == 0:
                if len(buy_orders):
                    del(buy_orders[0])
                if len(sell_orders):
                    del(sell_orders[0])
                buy_orders.append(o-LOW)
                sell_orders.append(o+HIGH)

    #print "balance: ", o, usdt_cnt, btc_cnt, usdt_cnt + btc_cnt*o
    #print "balance with init price:          ", usdt_cnt + btc_cnt*init_p
    #print "balance no trade:                 ", init_u + init_b*o
    return usdt_cnt + btc_cnt*o, usdt_cnt + btc_cnt*init_p, init_u + init_b*o, cnt

if __name__ == "__main__":
    # 350 150
    for low in range(180, 300, 20):
        for high in range(220, 300, 40):
            c,_, n, cnt = run(high, low)
            print "====== %f %f %02d High: %d Low: %d ======" % (c, n, cnt, high, low)
    #unit = 0.0005
    #while unit < 0.0031:
    #    print "====== %f unit %f ======" % (run(280, 200, unit), unit)
    #    unit += 0.0002


