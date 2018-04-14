from os import listdir
import pickle
import time

def sec2date(v):
    tt = time.localtime(v)
    return time.strftime("%Y-%m-%d %H:%M:%S", tt)

def read_pickle(path, extand, name=None):
    if name:
        with open(name,'rb') as f:
            d = pickle.load(f)
        return d

    filename_list = listdir(path)
    h = []
    for x in filename_list:
        if x.endswith(extand):
            h.append(x)
    h = sorted(h)

    d = []
    for f in h:
        with open(f,'rb') as f:
            d1 = pickle.load(f)
        d1.reverse()
        for i in d1[:-2]:
            if not (i in d):
                d.append(i)
    return d
