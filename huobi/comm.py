import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import randn
from pandas import Series, DataFrame

import datetime
import time
import os
from os import listdir
import pickle


KLINE_TT_COLS = ['id', 'open', 'high', 'low', 'close', 'amount', \
'count', 'vol']
csv_fname = "5min_kline_"

def sec2date(v):
    tt = time.localtime(v)
    return time.strftime("%Y-%m-%d %H:%M:%S", tt)

def datestr():
    tt = time.localtime()
    return time.strftime("%Y-%m-%d", tt)

def save_to_csv(df):
    name = csv_fname+datestr()+".csv"
    if not os.path.exists(name):
        df.to_csv(name)

def read_pickle(path, extand):
    filename_list = listdir(path)
    h = []
    for x in filename_list:
        if x.endswith(extand):
            h.append(x)

    pieces = []
    for f in h:
        with open(path+f,'rb') as f:
            d1 = pickle.load(f)
        frame = DataFrame(d1[2:], columns=KLINE_TT_COLS)
        pieces.append(frame)
    df = pd.concat(pieces)
    df = df.set_index('id')
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df.sort_index(inplace=True)
    return df
