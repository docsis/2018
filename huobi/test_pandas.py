#!/usr/bin/python
import datetime
import time
import pickle
import pandas as pd

KLINE_TT_COLS = ['id', 'open', 'high', 'low', 'close', 'amount']

read_file = open('kline.txt','rb')
d = pickle.load(read_file)
read_file.close()


def change(v):
    tt = time.localtime(v)
    return time.strftime("%Y-%m-%d %H:%M:%S", tt)

df = pd.DataFrame(d, columns=KLINE_TT_COLS)
#df['id'] = pd.to_timedelta(df['id'])
df['id'] = df['id'].apply(change)

print df

