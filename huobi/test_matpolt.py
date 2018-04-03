#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.pylab import date2num
import pickle


read_file = open('kline.txt','rb')
d = pickle.load(read_file)
read_file.close()

data_list = []

for block in d:
    dt = datetime.datetime.utcfromtimestamp(block['id']) + datetime.timedelta(hours=8)
    # mpf库中要求的顺序是：时间、开盘价、最高价、最低价、收盘价
    data_list.append((date2num(dt), block['open'], block['high'], block['low'], block['close']))


fig, ax = plt.subplots()
ax.xaxis_date()
ax.set_title('BTC/USDT')
mpf.candlestick_ohlc(ax,data_list,colorup='green',colordown='r',width=0.005)
plt.grid()
plt.show()


'''
fig, ax = plt.subplots(figsize=(15,5))
mpf.plot_day_summary_oclh(ax, data_list,colorup='g', colordown='r')
plt.grid(True)
ax.xaxis_date()
plt.title('wandayuanxian 17')
plt.ylabel('Price')
plt.grid()
plt.show()
'''

