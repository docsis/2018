#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import time
import pandas as pd
from comm import *

KLINE_TT_COLS = ['id', 'open', 'high', 'low', 'close', 'amount']

d = loaddict("./", "pickle")

def change(v):
    tt = time.localtime(v)
    return time.strftime("%Y-%m-%d %H:%M:%S", tt)

df = pd.DataFrame(d, columns=KLINE_TT_COLS)
#df['id'] = pd.to_timedelta(df['id'])
df['id'] = df['id'].apply(change)

print df

